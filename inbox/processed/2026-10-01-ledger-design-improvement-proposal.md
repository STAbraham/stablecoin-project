# Proposal: Ledger balance model and write-path improvements

**Status:** Proposed design; core balance model agreed in discussion with Steve.
**Purpose:** Handoff to an agent updating Shadow Ledger Redux and a second design document derived from it.
**Scope:** Preserve the journal model and business balance semantics while making account balances fast to read, straightforward to maintain, and independently reconstructable.

## 1. Context and source boundaries

The discussion referenced:

- [Shadow Ledger Redux](https://app.notion.com/p/zedfinancial/Shadow-Ledger-Redux-58f48642828d42f99fb9b8188d4e2b9c)
- [Balance Calculations](https://app.notion.com/p/d5f380c0aecc4994aab812d55c72c8ff)
- A second design document based on the original ledger design, whose title and URL have not yet been supplied.

This proposal summarizes the supplied conversation. It is not a fresh review of the current Notion pages or deployed implementation. The updating agent should read both current design documents and the linked balance page before editing, verify the described schema and lifecycle rules, and distinguish design intent from implemented behavior.

The original design, as described in the discussion, stores `posted_balance`, `pending_balance`, and `current_balance` at the account level and instructs writers to recompute them after journal changes. The linked balance notes use `pending_debits` and `pending_credits` to include both posted and active pending entries. Those definitions differ from the proposed definitions below.

“Recompute” is ambiguous: it could mean aggregating historical journal entries or simply evaluating formulas over already-maintained totals. The updated docs should explicitly describe each operation.

## 2. Core decisions

1. Keep ledger transactions and their debit/credit entries as the authoritative accounting record.
2. Maintain account-level aggregates synchronously, in the same database transaction as the journal changes they represent.
3. Persist four mutually exclusive buckets: posted debits, posted credits, pending-only debits, and pending-only credits.
4. Derive the three balances from those buckets. Do not maintain all seven values as independently writable fields.
5. Apply the contribution change caused by each journal event; do not rescan the account’s entire history on every write.
6. Retain independent journal aggregation for reconciliation, reconstruction, and migration.
7. Preserve the existing conservative authorization/current-balance policy for customer receivable accounts, subject to verification against the current docs.

## 3. What to preserve from the original design

The proposed optimization does not require replacing the fundamental ledger architecture:

- Separate ledger transactions from the entries that express their accounting effects.
- Preserve balanced debit/credit entries for each accounting transaction, within the applicable currency or accounting unit.
- Preserve posted accounting history; correct posted accounting through compensating entries rather than silently rewriting amounts.
- Retain grouping or linkage between authorizations, reversals, and clearing transactions.
- Retain the pending transaction discard/supersession model if confirmed in the current design.
- Retain account row locking around balance-dependent authorization decisions and balance updates.

If `discarded_at` or other lifecycle metadata is mutable, describe the journal accurately: immutable accounting amounts plus controlled lifecycle changes, rather than claiming that every field is immutable.

## 4. Proposed persisted state

| Direction | Active posted entries only | Active pending entries only |
| --- | --- | --- |
| Debit | `posted_debits` | `pending_debits` |
| Credit | `posted_credits` | `pending_credits` |

Each counter is the sum of entry amounts in exactly one bucket for that account. Determine status and active/discarded eligibility from the transaction or entry fields actually used by the schema. Exclude discarded or superseded contributions according to the verified lifecycle rules.

**Under this proposal, `pending_*` never includes posted entries.** This is a semantic change from the linked balance notes and must propagate to every formula and dependent consumer.

Account metadata includes `normal_balance`, constrained to `debit` or `credit`. A version and update timestamp may be useful for audit, concurrency, or reconciliation, but are implementation choices.

The counters may live on `ledger_accounts` or in a dedicated account-balance table. A separate table can support currency or other balance dimensions and isolate frequently updated state; it is not required for the optimization. Never mix different currencies into one set of totals without explicit conversion accounting.

Use exact monetary representations consistent with the existing ledger, such as integer minor units or appropriately constrained decimal values.

## 5. Derived balances

Define:

```text
PD = posted_debits
PC = posted_credits
UD = pending_debits   (unposted only)
UC = pending_credits  (unposted only)
```

| Balance | Debit-normal account | Credit-normal account |
| --- | --- | --- |
| `posted_balance` | `PD - PC` | `PC - PD` |
| `pending_balance` | `(PD + UD) - (PC + UC)` | `(PC + UC) - (PD + UD)` |
| `current_balance` | `(PD + UD) - PC` | `(PC + UC) - PD` |

Here, `pending_balance` retains the discussed legacy meaning: the projected balance including posted and active pending activity. It is **not** the net of pending-only entries. Pending-only net activity would instead be `UD - UC` for debit-normal accounts, or `UC - UD` for credit-normal accounts.

The credit-normal current-balance formula mirrors the rule of recognizing pending increases on the normal side while excluding pending decreases. Verify whether that policy is appropriate for every credit-normal account; a customer credit authorization rule should not automatically become a universal accounting policy.

For Zed’s debit-normal customer receivable account, `current_balance` recognizes pending purchases but does not release spending capacity for pending payments or refunds until posted. It is a business/risk measure derived from accounting state.

Consider documenting or renaming it as `authorization_balance` or `credit_exposure_balance`. Naming remains optional; changing the name must not silently change behavior or break dependent contracts. Credit availability may also depend on limits and other holds outside this formula.

### Example: pending payments do not release credit yet

| Activity | Amount |
| --- | ---: |
| Posted purchases | ₱8,000 |
| Pending purchases | ₱1,000 |
| Posted payment | ₱2,000 |
| Pending payment | ₱3,000 |

The counters are `PD = 8,000`, `PC = 2,000`, `UD = 1,000`, and `UC = 3,000`.

- Posted balance: ₱6,000.
- Pending/projected balance: ₱4,000.
- Current/authorization balance: ₱7,000.

Evaluate these expressions in a query, view, application getter, or database-generated column where supported. Generated columns are acceptable because they are derived automatically, rather than independently maintained by writers.

## 6. Why store four counters instead of three net balances?

Storing account-level balances was a sensible optimization. The important change is how that state is represented and maintained.

Net balances alone cannot recover gross debit and credit totals. Four separate buckets preserve both direction and lifecycle state, map directly to journal subsets, and expose offsetting discrepancies that might cancel in a net balance.

Incrementally maintaining three net balances could also be correct and efficient. The preference for four counters is about clearer semantics and stronger reconciliation visibility; constant-time maintenance comes from applying deltas, not from choosing four fields instead of three.

Pending-only counters also avoid mixing lifecycle states. Under the old inclusive definition, posting updates both the posted total and the inclusive pending total. Under the proposed model, posting removes the pending contribution and adds the posted contribution. This is primarily a clarity improvement, not a claim of a major database performance gain from one fewer arithmetic operation.

## 7. Atomic write path

For each logical ledger event, perform the following within one database transaction:

1. Establish or check the event’s idempotency identity so retries cannot duplicate journal or aggregate effects.
2. Lock affected account/balance rows in a consistent order. Lock relevant transaction groups or lifecycle rows as required by the existing model.
3. Read current state and perform any balance-dependent authorization decision while holding the necessary locks.
4. Validate the accounting entries and lifecycle transition.
5. Insert the new ledger transaction and entries; mark the appropriate prior pending contribution discarded/superseded when applicable.
6. Apply the net changes to all affected account counters.
7. Commit journal, lifecycle metadata, and counters together, or roll them all back.

The general update rule is:

```text
counter_delta = contribution_after_event - contribution_before_event
new_counter  = old_counter + counter_delta
```

This rule covers inserts, supersession, expiration, and reversals without aggregating historical entries. Apply it to every entry/account affected by the double-entry transaction, not just the customer account.

For an existing journal contribution, read and protect the state needed to establish whether it is still active. A repeated discard must not subtract the same contribution twice. An atomic increment alone does not protect a preceding read/check/authorize sequence.

### Why the lock matters

With ₱9,000 exposure and a ₱10,000 limit, two concurrent ₱800 authorizations must not both approve against the same ₱9,000 value. One writer locks, approves, updates to ₱9,800, and commits. The next writer then sees ₱9,800 and declines under that limit policy.

Keep journal processing and account updates short while holding locks. Shared settlement/control accounts can still create write contention even when each update is constant-time; this proposal does not resolve that separate scaling concern.

## 8. Lifecycle examples

The table shows the customer-side effect for a debit-normal receivable account. Corresponding entries and counters for other affected accounts must also be updated.

| Event | Counter changes |
| --- | --- |
| Create ₱100 pending purchase | `pending_debits += 100` |
| Replace that hold with a final ₱120 posted purchase | `pending_debits -= 100`; `posted_debits += 120` |
| Release/expire a remaining ₱100 hold | `pending_debits -= 100` |
| Reduce a ₱100 hold to ₱80 | Net `pending_debits -= 20`, reflecting the verified discard/replacement model |
| Post a ₱50 payment directly | `posted_credits += 50` |
| Create a ₱50 pending payment | `pending_credits += 50` |
| Post that pending payment for ₱50 | `pending_credits -= 50`; `posted_credits += 50` |
| Post a ₱20 refund against a posted purchase | `posted_credits += 20`, with compensating accounting entries |

Do not treat every presentment as releasing the entire original authorization. Partial capture, multiple presentments, incremental authorizations, unmatched presentments, and clearing amounts that differ from the hold require explicit remaining-hold rules. Derive each delta from the actual before/after contribution dictated by those rules.

The agreed example of ₱100 pending becoming ₱120 posted ends with `pending_debits = 0` and `posted_debits = 120`. Earlier discussion used an inclusive pending counter that ended at ₱120; that earlier recommendation is superseded.

## 9. Reconciliation and reconstruction

For each account and currency, independently aggregate the authoritative journal into the same four buckets and compare **each bucket**, not just net balances.

```text
stored posted_debits   == SUM(active posted debit entry amounts)
stored posted_credits  == SUM(active posted credit entry amounts)
stored pending_debits  == SUM(active pending debit entry amounts)
stored pending_credits == SUM(active pending credit entry amounts)
```

Run comparisons against a consistent snapshot or a defined version/cutoff so concurrent writes do not create false discrepancies. Define a safe repair/rebuild procedure that cannot overwrite newer live updates with an older aggregate.

Check transaction-level debit/credit equality separately. Matching account counters to their journal does not, by itself, prove that the journal transactions are balanced.

Choose reconciliation frequency based on operational needs. Full aggregation belongs in this independent verification path, historical reporting, and backfill—not in the routine authorization/write path.

## 10. Tradeoffs and migration considerations

Full recomputation is simple to reason about and avoids bespoke incremental transition logic. For small or low-traffic accounts it may be adequate, but its work grows with historical entry count and can extend the time locks are held. Incremental maintenance makes routine account balance reads and updates independent of history length, while requiring careful atomicity, idempotency, and lifecycle handling.

If this is only a design update, record these requirements without implying a live migration occurred. If an implementation already exists:

1. Identify consumers of all existing counter and balance definitions, including the second design doc.
2. Backfill the four exclusive buckets from a consistent journal snapshot.
3. Account for writes during backfill using a coordinated cutover or another explicit concurrency-safe method.
4. Compare each counter and confirm the derived balances preserve intended existing behavior.
5. Move writers and readers to the new semantics together, with an explicit compatibility strategy if needed.

Do not simply rename existing inclusive `pending_*` fields to pending-only fields without converting their values and updating dependent formulas.

## 11. Instructions for the updating agent

Read the current source pages and the second dependent design doc, then update their schema, terminology, formulas, and business flows consistently. Specifically:

- Replace ambiguous “recompute balances” instructions with “atomically apply the journal contribution delta to account aggregate counters.”
- Define `pending_debits` and `pending_credits` as pending-only everywhere.
- Preserve the existing meaning of the derived `pending_balance`, explicitly distinguishing it from pending-only net activity.
- Specify all normal-balance formulas and account-specific authorization policies.
- Make the pending-to-posted discard/replacement flow explicit, including remaining holds for partial or multiple captures.
- Document transactional boundaries, lock order, idempotency, and updates to all affected accounts.
- Add journal reconstruction and reconciliation invariants.
- Update examples, diagrams, API contracts, authorization checks, and assumptions in the dependent doc.
- Preserve unrelated product/accounting behavior; flag source contradictions rather than silently inventing lifecycle rules.

Details still to resolve from the source docs or implementation include the location of status/discard metadata, which accounts use the authorization formula, partial-clearing rules, idempotency keys, table placement, historical/as-of balance requirements, reconciliation cadence, and whether a live migration is needed.

### Acceptance criteria

The revised documents should let an implementing agent answer unambiguously:

1. What does each persisted counter include and exclude?
2. How is each balance derived for each account type?
3. What changes on auth, posting, reversal, expiration, payment, and partial capture?
4. Which changes commit atomically, and what happens on retry or concurrent authorization?
5. How are aggregates reconstructed and checked against the journal?
6. Do both design documents use the same definitions and preserve intended business behavior?

Validate with meaningful scenarios: changed clearing amounts, pending payment exclusion, partial/multiple captures, repeated events, duplicate discard attempts, concurrent authorizations, transaction rollback, and reconciliation against a consistent snapshot.

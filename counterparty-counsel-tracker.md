# Counterparty & Counsel Open Questions Tracker

**Status:** Live — Phase 0 artifact (created v5, 2026-08-28, per the 8/28 handoff memo)
**Purpose:** Single source of truth for partner-capability and legal confirmations. The PRD references items here by ID; the tech design must mark any section that depends on an open item `PENDING <id>`. **Working assumptions stay assumptions until confirmed here — do not silently promote them to facts in any doc.**

Statuses: `OPEN` · `ASKED` (question sent, awaiting answer) · `CONFIRMED` (written answer; link/quote the source) · `FAILED` (capability unavailable → trigger the named fallback decision).

## Bridge (owner: Steve ↔ Freddie Allen)

| ID | Question | Why it matters | Status | Fallback if FAILED |
|---|---|---|---|---|
| C-BR-1 | Is OUSD acquisition via Bridge a **true primary mint per customer transaction**, and can it mint **directly to an arbitrary customer-owned Privy address**? | Load-bearing for the whole on-ramp characterization (D4, R27). Public Bridge docs cover transfers/wallets generally; OUSD-specific mint behavior unverified. | OPEN | Escalate to Steve + counsel — do **not** fall back to Zed-inventory resale without legal approval (R27). |
| C-BR-2 | Can OUSD be **redeemed/burned directly from the customer wallet** (customer-signed) without transferring to a Zed wallet? | Load-bearing for the off-ramp (D6, R30). | OPEN | Fallback decision: licensed PH VASP off-ramp, or defer PH off-ramp. **Never** customer → Zed-wallet. |
| C-BR-3 | Do `on_behalf_of` / customer records / liquidation addresses give **per-operation, per-customer attribution** of redemption proceeds settling into Zed's prefunded/settlement balance? | R33 attribution + R14 ledger fields; also the offshore-access analysis (C-LC-3) leans on Bridge being Zed's counterparty. | OPEN | Manual attribution via operation references; revisit architecture with counsel if attribution is impossible. |
| C-BR-4 | Can Bridge support **reward-related incremental OUSD mints directly to end-user wallets** (Zed-funded)? | Preferred Zed Rewards fulfillment (D5, §6.3). | OPEN | Zed payout-wallet → user-wallet transfers, gated on legal sign-off. |
| C-BR-5 | OUSD supported chains (Base availability) + can the **$500 entity test cap** be raised for internal alpha? | D6b; week-3 alpha realism. | OPEN | Ship on whatever chain OUSD launches with; keep alpha under cap. |

## Privy (owner: Steve)

| ID | Question | Why it matters | Status | Fallback if FAILED |
|---|---|---|---|---|
| C-PR-1 | Confirm wallet configuration where the **user is the owner**, with **recovery/export** usable independently of Zed, and **no Zed signer/owner/export capability** at any time. | D3, R31 — the self-custody characterization collapses without it. | OPEN | Evaluate alternative embedded-wallet configs/providers; architecture does not proceed on a Zed-signer model. |
| C-PR-2 | Contract + sandbox access timeline. | Week-1 build dependency. | OPEN | — |

## Netbank (owner: Steve)

| ID | Question | Why it matters | Status | Fallback if FAILED |
|---|---|---|---|---|
| C-NB-1 | Disburse-to-Account scope + sandbox credentials enabled on Zed's account. | D9b payout rail; week-2 build. | OPEN | Manual bank-portal payouts with dual approval (documented runbook) for wave 1. |
| C-NB-2 | Second virtual collection account per user supported under the current agreement. | D9a collection separation. | OPEN | Reference-code matching on the existing VA (weaker; reopens D9a). |

## Open Standard (owner: Steve, via Freddie/OS contact)

| ID | Question | Why it matters | Status | Fallback if FAILED |
|---|---|---|---|---|
| C-OS-1 | Confirm **user-owned** Privy wallets register under the **Relationship** test and that registration is an attribution/compliance construct only (no custody implication, no direct PH-retail relationship with OS/Bridge). | D5/§6.3 Marketing Fee accrual on user balances; feeds C-LC-3. Rewards doc language ("wallet you provisioned for a direct customer") fits; Earning Equity doc words it as "custodies OUSD on your behalf" — wording matters legally, so confirm. | OPEN | Register only Zed-owned wallets; re-underwrite Zed Rewards economics without user-balance accrual. |
| C-OS-2 | Marketing Fee **payout token and destination** (on-chain per Rewards doc — OUSD? to which designated wallet?), and whether Bridge takes an additional cut. | Booking as Zed revenue (C-AC-1); treasury handling of the payout wallet. | OPEN | Handle whatever asset arrives via treasury runbook; economics re-checked. |
| C-OS-3 | Dashboard/API access for wallet registration (API key "available Sept 2026") — can Zed register wallets **now** (accrual is not backdated)? CSV path in the interim? | Every week unregistered = accrual permanently lost (§2a). | OPEN | CSV upload via OS contact until API access. |

## Counsel (owner: Open Question #8 — unassigned)

| ID | Question | Why it matters | Status | Fallback if FAILED |
|---|---|---|---|---|
| C-LC-1 | **BSP posture:** does the PHP↔OUSD issuance/redemption activity, as architected in PRD v5 (distributor/agent, no custody, no customer fiat balances, no spread), trigger VASP registration or FX licensing? Written opinion required (R34). | Launch blocker. | OPEN | StratBox engagement / architecture revision / launch hold. |
| C-LC-2 | **SEC path:** offering a stablecoin product to PH retail — CASP analysis; no-action/interpretive confirmation, exemption, or StratBox relief (R34). | Launch blocker. | OPEN | Same as C-LC-1. |
| C-LC-3 | **BSP M-2026-003 offshore-access rule:** confirm that Bridge/OS customer + `on_behalf_of` records are compliance/attribution constructs and do not constitute prohibited direct PH retail access to an offshore VASP; assess D11 (US/EU off-ramp) against the same rule. | R33; D11 ships or dies on this. | OPEN | Restrict to PH off-ramp only; strip D11. |

## Accounting (owner: Steve / finance)

| ID | Question | Why it matters | Status | Fallback if FAILED |
|---|---|---|---|---|
| C-AC-1 | Confirm booking treatment: Marketing Fee as Zed revenue; Zed Rewards as program expense/liability (not customer property pass-through). | D5 separation is both a legal and an accounting position. | OPEN | Adjust ledger accounts (§6.8) per advice. |

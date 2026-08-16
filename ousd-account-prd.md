# Zed Dollar Account (OUSD) — Product Requirements Document

**Status:** Draft v4 — decisions D1–D11 settled; remaining open items are §10 business questions
**Date:** 2026-08-16
**Product:** Zed stablecoin store-of-value account, piloting on **Open Standard's OUSD**
**Scope:** MVP pilot ("PoC") for 50 of Zed's ~11,000 credit cardholders
**Timeline:** **3–4 week build target** (external launch gated on OUSD public launch, targeted 9/15/26)

**Changelog v1 → v2:** Switched from a Zed-branded white-label stablecoin (USDZ) to **OUSD** (Open Standard's stablecoin, accessed via Bridge). Bridge requires a committed minimum mint (typically many millions of dollars) for any white-label coin — not viable for a 50-user PoC. If the PoC succeeds, revisit white-label vs. continuing on OUSD at the scale-up decision gate. Source: Bridge email thread with Frederick Allen, `Zed - Bridge Email Thread (8.16.26).pdf` in this folder.

**Changelog v3 → v4:** All remaining architecture decisions settled after code + vendor verification: (1) **D9a** — collections via a *second* per-user Netbank virtual collection account dedicated to stablecoin funding (verified: today's webhook posts every VA credit as a card payment, so purpose-separation must happen at the VA level). (2) **D9b** — payouts via Netbank's Disburse-to-Account API (net-new integration, ~2–4 days; InstaPay < ₱50k real-time, PESONet above; manual bank-portal payout is the fallback runbook, and the Netbank disburse scope/sandbox confirmation is a Phase 0 gate). (3) **D10** — pre-funded floats with *manual* daily FX (dual-controlled, on the venue's own interface — no dependency on the distrusted Coins.ph API code). (4) **D11 (new)** — US/EU off-ramp stays in scope but gated per-user and sequenced as a week-4 stretch; it's cheap because Bridge redemption exists for treasury anyway. (5) New requirement R12a: destination bank accounts encrypted at rest, masked everywhere, materialized only at disbursement time.

**Changelog v2 → v3:** (1) D7 settled: mobile-responsive web app embedded as a webview tab in the existing native apps, built to graduate to React Native post-MVP. (2) D8 settled: bounded module in `zed-rust-api`, with an explicit caution that the existing Coins.ph USDC code is *reference material and an FX venue*, not a foundation (its wallet/subaccount structure is Coins.ph-domain and it does not track balances). (3) New hard requirement: lightweight **double-entry ledger over Zed-controlled funds** (§6.8) — user balances are on-chain (source of truth) and reconciled, not ledgered as liabilities. (4) Yield mechanics corrected after external verification: OUSD yield is distributed **to the platform (Zed), not directly to holder wallets** — Zed builds the user pass-through; attribution of Privy wallets to Zed's platform is a new confirm-with-Bridge item. (5) Rollout compressed to a 3–4 week build plan.

---

## 1. Summary

Zed will launch a dollar-denominated store-of-value account for Philippine customers, built on **OUSD** (Open Standard's yield-bearing stablecoin, distributed via **Bridge.xyz**), held in **self-custody embedded wallets powered by Privy**. Users fund the account with Philippine pesos (PHP); Zed converts to USD and acquires OUSD into the user's wallet. Users earn rewards — OUSD rewards are distributed to the platforms where OUSD is held, so Zed receives the yield on its users' balances and passes it through — and can off-ramp at any time to a Philippine bank account via InstaPay/PESONet, or to US/EU bank accounts via Bridge's native rails.

**Zed's unique value-add is the PHP leg** — on-ramp collection, PHP↔USD treasury management, and off-ramp disbursement to Philippine banks. Everything else (the stablecoin itself, reserve management, US/EU rails, wallet infrastructure) is delegated to Open Standard, Bridge, and Privy.

### Why this product

- PHP has persistently depreciated against USD; middle-class Filipinos want dollar savings but face high minimums, paperwork, and poor rates at traditional banks for USD accounts.
- Zed's cardholders are already KYC'd (Persona), credit-underwritten, and transacting with us — a trusted brand relationship to extend into savings.
- OUSD reserve yield (≈ Treasury yield; Open Standard's fee capped at 25bps of yield, expected lower at launch) lets us offer a rewards rate on dollar balances that domestic PHP savings products can't match.
- Strategic: diversifies Zed from mono-line credit into a deposit-like relationship, increasing retention and lifetime value.

### Why OUSD (not our own coin, yet)

Bridge's white-label issuance requires a contractual minimum mint commitment (many $M) because their fee comes from reserve yield. For a 50-user PoC, OUSD gives us the identical product mechanics — mint/redeem via Bridge, reserve-yield rewards, multi-chain support — with no mint commitment. Branding is the trade-off: the token is OUSD, and the *account experience* is Zed's (see Open Question #9 on product naming). White-label becomes a scale-up decision if the PoC succeeds.

### External timeline constraints (from Bridge, as of 8/14/26)

- OUSD is **live for testing now, capped at $500 total for Zed** (entity-level cap, not per end user; testing means Zed testing, not Zed's users).
- Open Standard targets **9/15/2026 for public OUSD launch** — external pilot users cannot be funded at real size before then.
- **Immediate action:** complete Bridge KYB (link in Freddie's 8/14 email) so Bridge can progress approval and spin up access.

---

## 2. Goals & success metrics (pilot)

| Goal | Metric | Target |
|---|---|---|
| Validate demand | Pilot users who complete ≥1 on-ramp | ≥ 35 of 50 (70%) |
| Validate store-of-value behavior | 30-day balance retention (balances held, not immediately off-ramped) | ≥ 60% of deposited value retained at day 30 |
| Validate repeat usage | Users with ≥2 on-ramps in first 60 days | ≥ 40% |
| Operational soundness | On-ramp funds → OUSD in wallet median time | ≤ 30 min during business hours *(proposed)* |
| Operational soundness | PH off-ramp request → PHP received median time | ≤ 1 business day *(proposed)* |
| Zero-loss bar | Reconciliation breaks unresolved > 24h; user funds lost | 0 |
| Rewards work | Rewards accrue and post correctly for 100% of holders | 100% |

Secondary learning goals: real FX + rails cost per transaction, treasury float sizing, support ticket volume/themes, demand for US/EU off-ramp, realized net yield after Open Standard's fee (validates white-label economics for the scale-up decision).

---

## 3. Non-goals (explicitly out of MVP)

1. **Payments / spend from OUSD** — no card funding, bill pay, P2P transfers, or merchant payments from the balance. Store of value only.
2. **External crypto transfers** — no sending OUSD to external wallets and no depositing crypto from outside the Zed ecosystem. Note: OUSD is a public token, so this is enforced at the product/UI layer (Zed's app is the only interface to the Privy wallet), not at the token layer — see §8.
3. **Non-cardholders** — pilot is invite-only from the existing cardholder base.
4. **Other stablecoins/assets** — OUSD only. No USDC/USDT balances shown, no trading.
5. **Scale** — 50 users. Manual/semi-manual ops steps are acceptable where they buy speed to launch (documented in runbooks).
6. **Native mobile UI** — MVP ships as a web app (Decision D7). Native iOS/Android integration comes post-validation.
7. **Paying the Zed card bill from the balance** — natural follow-on, deliberately excluded from MVP to keep the money surface minimal.
8. **White-label stablecoin** — deferred to the post-pilot decision gate.

---

## 4. Decisions

### Settled (per Steve / Bridge thread)

| # | Decision | Choice |
|---|---|---|
| D1 | Product core | Store of value: hold OUSD, earn rewards, on/off-ramp. No spend. |
| D2 | Stablecoin | **OUSD** (Open Standard), accessed via **Bridge.xyz**. White-label revisited post-pilot. *(Changed in v2; was Zed-branded USDZ.)* |
| D3 | Custody | **Self-custody** via **Privy** embedded wallets (no seed phrases surfaced; Zed never custodies user assets) |
| D4 | On-ramp | Zed-built PHP leg: user sends PHP → Zed converts to USD → OUSD delivered to user's wallet via Bridge |
| D5 | Rewards | OUSD reserve yield is distributed **to Zed as the distributing platform** (per Freddie 8/12 and public Open Standard reporting: partner-level distribution, likely as USD payouts proportional to OUSD pushed/held — **not** paid on-chain to holder wallets). Zed builds the user pass-through and pays users in OUSD. Open Standard fee ≤ 25bps of yield. Exact mechanics (payout currency, destination, cadence, wallet attribution) unverified — Open Question #1; design must tolerate either mechanic. |
| D6 | Off-ramp | PH banks via **InstaPay/PESONet** (Zed-built, the differentiator); US/EU bank accounts via Bridge's native off-ramps (see Bridge virtual-accounts and one-time-payment guides) |
| D6a | KYC | Reuse existing **Persona** KYC; share data with Bridge so pilot users don't re-KYC |
| D6b | Chain | EVM L2 preferred, **Base** the leading candidate (Steve: solving for cost + speed; Bridge supports Base, Solana, Sui, Aptos, HyperEVM, Ethereum, Arbitrum, Optimism, Polygon, Linea, Monad, Abstract, Tempo). Confirm OUSD's default/supported chains with Bridge in tech design. |

### Settled in v3 (per Steve, 8/16)

| # | Decision | Choice | Notes |
|---|---|---|---|
| D7 | Client surface | **Mobile-responsive web app, embedded as a webview tab inside the existing native apps.** Built in React with React-Native-portable patterns (shared design tokens, RN-compatible state/navigation structure, no web-only UI paradigms in core flows) so it can graduate to an in-app React Native section post-MVP. | Session hand-off from the native app to the webview (so users are seamlessly authenticated) is a first-class tech-design item. Web deploys iterate daily with no app-store cycle during the pilot. |
| D8 | Backend home | **New bounded module inside `zed-rust-api`** (own tables, own route namespace, feature-flagged; no foreign keys into card tables beyond `user_id`). | Reuses auth/sessions (critical for the D7 webview), users table, Persona artifacts, deploy/CI/workers, incoming-payments matching, QRPH collections, and in-repo integration patterns. **Caution (Steve):** the existing Coins.ph USDC code is *not* a foundation — its wallet addresses and subaccount structure are Coins.ph-domain artifacts, and it does not genuinely track/manage balances. Treat it as (a) the FX/conversion venue behind a clean interface and (b) reference for house patterns. The OUSD module owns its own money tracking (§6.8). |

### Settled in v4 (per Steve + code/vendor verification, 8/16)

| # | Decision | Choice | Rationale |
|---|---|---|---|
| D9a | PHP collections | **Second per-user Netbank virtual collection account, dedicated to stablecoin funding.** Verified in code: each user already gets a Netbank VA (`bill_pay_info.reference_id`) with QRPH generated against it, and the webhook posts *every* credit to it as a card payment. A second, purpose-dedicated VA per user cleanly separates card bill-pay from OUSD funding — the webhook routes by which VA was credited. | Reuses the live, proven collection rail these exact users already use; the only change is a purpose dimension on VA issuance and a branch in the webhook. |
| D9b | PHP payouts | **Netbank Disburse-to-Account API in MVP** (net-new integration — no disbursement code exists today; the current Netbank client only does QRPH + auth). Single endpoint; real-time InstaPay < ₱50k; PESONet for larger. Same vendor and auth pattern as collections; sized ~2–4 days incl. payout state machine. **Manual bank-portal payout with dual approval is the documented fallback runbook**, not the primary path. Phase 0 gate: confirm disburse scope + sandbox credentials on Zed's Netbank account. | One vendor for both PHP legs; VAs collect in, settlement account disburses out (PHP passthrough). If the Phase 0 capability check fails or slips, fall back to manual payouts for wave 1 without changing user-facing flow. |
| D10 | Treasury/FX | **Pre-funded floats + manual daily FX with dual control.** USD float at Bridge, PHP float at Netbank; ramps execute instantly against floats; ops rebalances daily by executing FX manually on the venue's own interface (Coins.ph dashboard or bank), dual-approved, recorded in the ledger. Deliberately **no dependency on the Coins.ph API code** (per D8 caution). Automation is a post-MVP upgrade. | Instant-feeling UX; FX exposure bounded and trivial at pilot caps (worst case ≈ full pilot TVL < 1 day). Manual execution removes the least-trusted integration from the money path. |
| D11 | US/EU off-ramp | **In scope, gated per-user ("contact support to enable"), sequenced after PH flows are green** (week-4 stretch). Only to destinations where Bridge has existing fiat off-ramps. | Cheaper than originally framed: Bridge redemption (OUSD→USD) is built for treasury regardless, so the US/EU leg is external-account registration + a Bridge transfer call — no FX, no local rail, no float. ~2–4 days incremental; the gate contains support/test surface during the pilot. |

---

## 5. Users & eligibility

- **Pilot cohort:** 50 users, invite-only, selected from the ~11,000 active cardholders.
- **Proposed eligibility criteria** *(confirm — Open Question #3)*: account in good standing (not delinquent), Persona KYC completed at a tier sufficient for Bridge's requirements, active app usage in the last 90 days, and opt-in via waitlist/invitation.
- Users must accept new terms: Zed Dollar Account terms of service, Bridge's end-user terms, applicable OUSD/Open Standard terms, and Privy's terms, with clear self-custody and no-deposit-insurance disclosures (this is not a bank deposit; not PDIC-insured; OUSD is issued by Open Standard, not Zed).
- If a pilot user becomes delinquent on their card, their OUSD remains theirs (self-custody — Zed cannot seize it). Proposed policy: freeze *new on-ramps* for delinquent users; off-ramp remains available. *(Confirm — Open Question #7.)*

---

## 6. Product requirements

### 6.1 Onboarding / account opening

1. Invited user opens the web app and authenticates with their existing Zed credentials (same auth as the mobile apps, via zed-rust-api).
2. User reviews and accepts terms and self-custody + risk disclosures.
3. Behind the scenes, Zed:
   - Creates a **Bridge customer** using shared Persona KYC data. If Bridge requires additional fields, the user completes only the delta.
   - Provisions a **Privy embedded wallet** (keys secured by Privy's infrastructure; user recovery per Privy's model — no seed phrase UX).
   - Registers the wallet address with the account module.
4. User lands on a zero-balance home screen with a clear "Add dollars" call to action.

**Requirements:**
- R1. Onboarding must complete in a single session, < 5 minutes for a user whose Persona KYC transfers cleanly.
- R2. If Bridge KYC fails or needs review, the user sees a "we're reviewing your account" state; ops is alerted (Slack), and the user is notified when resolved.
- R3. All consents (terms versions, timestamps) are recorded per user.

### 6.2 On-ramp (PHP → OUSD)

1. User taps "Add dollars," sees an indicative rate (all-in, spread included) and enters a PHP amount within limits.
2. Zed presents payment instructions: a QRPH code generated against the user's **stablecoin-dedicated Netbank virtual account** (per D9a — distinct from their card bill-pay VA, so funding intent is unambiguous), plus the VA number for manual bank transfer.
3. User pays from their own bank/e-wallet app. Zed's incoming-payments pipeline detects and matches the deposit.
4. On match, Zed locks the conversion at the quoted rate (within a validity window — see Open Question #2 on quote/rate policy), debits the USD float, and acquires OUSD to the user's Privy wallet via Bridge.
5. User sees pending → completed states, push/email notification on completion, and the OUSD credit in their activity feed.

**Requirements:**
- R4. Median deposit-detection-to-delivery ≤ 30 min during business hours; hard SLA of same business day. Deposits outside business hours process next window *(if D10's float model permits 24/7, better — tech design decides)*.
- R5. Unmatched or out-of-limit deposits alert ops within 15 minutes; refund-to-source is the documented default remedy.
- R6. Every on-ramp records: PHP received, FX rate applied, spread taken, USD funded, OUSD delivered, on-chain tx hash — reconcilable end to end in the ledger.
- R7. Limits enforced at quote time and at match time (per-user and pilot-wide caps, §8).

### 6.3 Holding & rewards

1. Home screen shows: OUSD balance (presented as a dollar balance), PHP-equivalent at current indicative rate, lifetime rewards earned, and current rewards rate (APY-style, clearly labeled "variable").
2. Rewards: OUSD yield is distributed to Zed as the distributing platform (likely USD payouts proportional to OUSD pushed/held — mechanics per Open Question #1); Zed passes it through to users **in OUSD** on a fixed schedule (proposed: accrue daily, distribute monthly). If platform payouts arrive in USD, the pass-through includes converting the payout to OUSD before distribution.
3. Activity feed shows every event: on-ramps, off-ramps, rewards distributions.

**Requirements:**
- R8. Rewards math is deterministic and auditable: each distribution records the balance snapshot(s), rate, period, and resulting OUSD amount per user; totals reconcile against platform yield actually received from Open Standard/Bridge for the period (whatever its currency/mechanic).
- R8a. User-balance snapshots for accrual are taken from on-chain wallet balances (source of truth), not from an internal running balance.
- R9. Rate displayed is Zed's pass-through rate (gross OUSD yield minus Open Standard's fee (≤25bps) minus Zed's margin — Open Question #1 sets the split), updated whenever the upstream rate changes.
- R10. Marketing/UX language must not call rewards "interest" or the product a "deposit/savings account" without compliance sign-off (Open Question #8).

### 6.4 Off-ramp — Philippine bank (the differentiator)

1. User taps "Withdraw," chooses "Philippine bank account," enters/selects a destination account (bank + account number, InstaPay or PESONet routing chosen automatically by amount/bank), and an amount within limits.
2. Zed shows the all-in PHP the user will receive (rate + any fee) and asks for confirmation.
3. On confirm: user authorizes the OUSD transfer from their Privy wallet (Privy signing UX) to Zed's redemption address → Zed redeems via Bridge (OUSD → USD to Zed's account) → Zed pays PHP from the local float to the user's bank via the **Netbank Disburse-to-Account API** (per D9b: InstaPay < ₱50k real-time, PESONet above; manual bank-portal payout with dual approval is the fallback runbook).
4. States: requested → OUSD received → PHP sent → completed, with notifications. Failures (bad account number, rail rejection) surface to the user with ops alerting.

**Requirements:**
- R12a. **Destination account storage:** account numbers encrypted at rest (app-level), rendered masked everywhere (UI, logs, Slack alerts, ops dashboard), full value materialized only at disbursement call time. (Existing Brankas-linked account storage is effectively plaintext — do not copy that pattern.) Account holder name + bank code stored alongside for name-match checks.
- R11. Median request-to-PHP-received ≤ 1 business day; InstaPay-eligible amounts (≤ ₱50k) should typically land same day.
- R12. First off-ramp to a new destination account may require a verification step (proposed: micro-confirmation of account-holder name match where the rail returns it) — anti-misdirection, not anti-fraud theater.
- R13. Destination account holder must be the user themselves for MVP (name-match policy; third-party payouts excluded — reduces mule/AML surface).
- R14. Every off-ramp records: OUSD redeemed, USD received, FX rate, spread, PHP sent, rail used, rail reference — ledger-reconcilable end to end.

### 6.5 Off-ramp — US/EU bank (via Bridge)

1. Same entry point; user selects "US bank (USD)" or "EU bank (EUR/SEPA)," provides account details, Bridge handles the transfer from redeemed OUSD (per Bridge's virtual-accounts / one-time-payment rails).
2. Zed passes through Bridge's rails, fees, and timelines transparently.

**Requirements:**
- R15. Gated per-user behind "contact support to enable" (per D11); built as a week-4 stretch after PH flows are green. Only destinations with existing Bridge fiat off-ramps are offered. Since Bridge redemption (OUSD→USD) exists for treasury regardless, this leg is external-account registration + a Bridge transfer call — no FX, no local rail, no float.
- R13 (name-match: user's own account) and R12a (encrypted storage, masked rendering) apply here too.

### 6.6 Notifications & comms

- R16. Transactional notifications (email + push via existing channels) for: onboarding approved, deposit received, OUSD delivered, withdrawal stages, rewards posted.
- R17. A pilot-support channel (existing in-app support / concierge Slack-backed flow) with a dedicated runbook for account issues.

### 6.7 Ops & internal tooling

- R18. **Ops dashboard** (internal, can be minimal/admin-grade): pending on-ramps and off-ramps with state, unmatched deposits, float balances (PHP, USD at Bridge, OUSD rewards pool), manual retry/resolve actions with audit log.
- R19. **Dual control** on any manual money movement (treasury rebalance, manual disbursement, refund): initiated by one operator, approved by a second. At pilot scale this can be a Slack-approval flow, but it must exist from day one.
- R20. **Daily reconciliation** job + report: internal ledger vs. Bridge balances vs. on-chain OUSD per wallet vs. bank/rail statements vs. Coins.ph (if used for FX). Any break pages ops; unresolved > 24h breaches the pilot's zero-loss bar (§2).
- R21. **Runbooks** written before launch: stuck on-ramp, stuck off-ramp, Bridge outage, Privy outage, rail outage, FX venue outage, user-reported missing funds, pilot halt procedure ("close the ramp": disable on-ramps while keeping off-ramps working).

### 6.8 Money tracking & ledger *(added in v3 — hard requirement)*

The zero-loss bar (§2) is enforced by construction, not by hope. The existing Coins.ph/USDC work explicitly does **not** meet this bar (no balance tracking on our side) and is not the pattern to follow.

- R22. **Lightweight double-entry ledger over Zed-controlled funds.** Accounts (indicative): PHP float, USD float at Bridge, PHP-in-flight (deposits matched, OUSD not yet delivered), USD/OUSD-in-flight (redemptions received, PHP not yet paid), FX spread revenue, rewards pool (yield received, not yet distributed), rewards payable. Every on-ramp, off-ramp, treasury rebalance, and rewards event posts balanced entries; the ledger is append-only. This is ~8–10 accounts and balanced postings — deliberately small, deliberately double-entry.
- R23. **User balances are NOT ledger liabilities.** Users self-custody OUSD; the chain is the source of truth for user balances. The ledger tracks only money Zed controls or is mid-flight on. This is what keeps R22 small enough for the 3–4 week timeline.
- R24. **Per-operation state machines** with an immutable event trail for every ramp (per R6/R14); no operation can silently disappear — terminal states are only `completed`, `refunded`, or `failed-with-ops-resolution`.
- R25. **Daily reconciliation ties the three worlds together** (extends R20): ledger balances vs. Bridge/bank/FX-venue statements vs. on-chain OUSD across user wallets (expected-from-operations vs. actual). Any drift is a paged break.
- R26. The existing `shadowledger` service is **evaluated, not assumed**, in tech design: reuse it only if its posting model fits cleanly; if it is card-domain-tied, build standalone tables for this module.

---

## 7. Treasury requirements (per D10)

- T1. USD float pre-funded at Bridge sized to ≥ 1 typical day of on-ramps (initial proposal: $25k, revisit weekly); PHP float at disbursement partner sized to ≥ 2 typical days of off-ramps (initial proposal: ₱1.5M).
- T2. Daily rebalancing: net PHP collected converted to USD and vice versa, executed **manually by ops on the FX venue's own interface** (Coins.ph dashboard or bank; tech design confirms the exact PHP→USD→Bridge funding route), dual-controlled, and recorded in the ledger. Per D10, the Coins.ph API code is not in the money path; automation is a post-MVP upgrade.
- T3. FX spread charged to users is a configuration value (basis points over reference rate), set per Open Question #4; every transaction records reference rate, applied rate, and captured spread.
- T4. Float thresholds alert ops (Slack) when below 0.5 days of expected volume; on-ramp quoting pauses gracefully ("deposits temporarily delayed") if the USD float cannot cover pending deliveries.
- T5. Weekly treasury report: float levels, FX P&L (spread captured vs. rebalancing cost), rewards received vs. distributed.

---

## 8. Limits, compliance & risk posture

**Proposed pilot limits** *(all confirmable — Open Question #6; note the $500 entity-wide cap applies to pre-9/15 testing only)*:

| Limit | Proposed value |
|---|---|
| Min on-ramp | ₱1,000 |
| Max single on-ramp | ₱100,000 |
| Max per-user balance | ₱500,000 equivalent (≈ $8,700) |
| Max per-user monthly on-ramp | ₱500,000 |
| Pilot-wide TVL cap | ₱15M equivalent (≈ $260k) |
| Off-ramp | No minimum beyond rail minimums; max = full balance |

**Compliance posture (to be validated with counsel — Open Question #8):**
- Self-custody via Privy + OUSD issued by Open Standard (reserves managed upstream, distributed via Bridge, a licensed US entity) + fiat legs through BSP-supervised partners (existing bank/EMI partners; Coins.ph is a BSP-licensed VASP) is the structure that minimizes Zed's own licensing surface. Using a third-party public stablecoin arguably positions Zed *further* from "issuer" than white-label would. Whether Zed's PHP↔OUSD exchange activity itself triggers BSP VASP registration is **the** legal question to answer before launch — flagging as a launch blocker to resolve in parallel with the build, not after it.
- **Closed-loop is product-enforced, not token-enforced** *(changed in v2)*: OUSD is a public token, so Zed cannot allowlist transfers at the token level. The closed loop rests on (a) Zed's app being the only interface to the Privy embedded wallet, with no external-send/receive UI, and (b) ignoring any unsolicited external deposits in the displayed balance (policy for handling them: tech design). Confirm with Privy what wallet-level controls exist. Residual risk accepted for a 50-user invite-only pilot.
- Own-account-only fiat legs (R13) keep AML/travel-rule surface minimal for MVP.
- Existing transaction-monitoring obligations extend to this product: on/off-ramp events feed the same monitoring/alerting used for card payments (Comply Advantage screening where applicable).
- Clear user disclosures: not a bank deposit, not PDIC-insured, variable rewards, FX risk on the PHP value of holdings, self-custody model, OUSD issued by Open Standard.

**Key product risks:**

| Risk | Mitigation |
|---|---|
| Regulatory: PHP↔OUSD exchange deemed licensable VASP activity | Counsel review pre-launch (launch blocker); partner-heavy structure; 50-user invite-only pilot framing |
| OUSD/Open Standard dependency (new issuer; public launch slips past 9/15; depeg or reserve issues) | Timeline buffer in rollout; monitor OUSD launch readiness via Bridge; off-ramp-priority halt procedure; scale-up gate re-evaluates issuer choice |
| FX exposure on floats | Caps + daily rebalancing + small float sizing (T1–T4) |
| Reconciliation break / lost funds | Ledger-first design, daily recon (R20), dual control (R19), zero-loss bar |
| Bridge or Privy outage/dependency | Runbooks (R21); "close the ramp" procedure; off-ramp-priority recovery |
| User confusion about self-custody / recovery | Privy's recovery UX + explicit onboarding education screen; pilot concierge support |
| Users discover OUSD is externally transferable (public token) despite closed-loop UI | UI-only wallet interface, no external send/receive surface; Privy wallet-control confirmation; pilot-scale monitoring of on-chain activity on user wallets |
| Rewards mislabeling as interest → regulatory exposure | R10 language review |

---

## 9. Rollout plan — 3–4 week build

Anchors: build starts **week of 8/18**; Open Standard's public OUSD launch targeted **9/15/2026** (per Bridge, 8/12/26). The build target and the OUSD launch date land in the same week — external users are gated on whichever is later.

**Phase 0 — Partner & legal track (immediately, parallel to build):**
- Complete **Bridge KYB** (action owner: Steve — link in Freddie's 8/14 email; Freddie progresses approval on completion). This gates OUSD test access, so it's the #1 external dependency.
- Privy contract + sandbox access.
- Confirm with Freddie: OUSD acquire/redeem API surface, chains (Base availability), rewards mechanics + wallet attribution (Open Question #1), whether the $500 test cap can be raised for internal alpha, Persona→Bridge KYC sharing.
- **Netbank commercial asks (this week):** confirm Disburse-to-Account scope + sandbox credentials are enabled on Zed's account, and confirm issuing a second virtual collection account per user is supported under the current agreement.
- Counsel opinion on BSP posture kicked off (Open Question #8) — must not land after wave 1.

**Week 1 (8/18) — Foundations:** backend module skeleton (tables, ledger per §6.8, operation state machines, feature flag), Bridge + Privy sandbox clients, web app skeleton with auth/session hand-off from the native apps (webview), onboarding flow against sandbox.
**Week 2 (8/25) — Money flows:** on-ramp end-to-end in sandbox (QRPH/reference deposit → match → FX lock → OUSD delivery), off-ramp end-to-end (OUSD redemption → InstaPay/PESONet payout), reconciliation job v1, minimal ops dashboard + dual-control approvals.
**Week 3 (9/1) — Hardening + internal alpha:** rewards accrual/distribution job, notifications, runbooks, real-money internal alpha under the **$500 entity-wide test cap** (a handful of employees, small amounts), daily recon running clean.
**Week 4 (9/8–9/15) — Polish + launch readiness:** alpha fixes, limits enforcement verified, counsel/compliance check-in, wave-1 user selection and comms prepared. **At OUSD public launch (≈9/15): Phase 2.**

**Phase 2 — Pilot wave 1 (post-9/15):** 15 external users at real limits. Exit: ≥ 10 funded accounts, no unresolved recon breaks, support load acceptable.
**Phase 3 — Full pilot:** all 50 users. Runs ≥ 60 days against §2 metrics.
**Decision gate:** scale (React Native in-app section per D7's groundwork, higher caps, more users, **white-label stablecoin vs. staying on OUSD** — revisit minimum-mint economics with Bridge using realized pilot AUM), pivot, or wind down (wind-down = off-ramp everyone, a first-class documented flow).

Timeline risks called out honestly: KYB/partner-access delays directly eat build weeks (sandbox access is needed by week 1); OUSD public launch slipping past 9/15 delays wave 1 but not the build; the counsel opinion is the only item that can block launch with the build finished.

---

## 10. Open questions (need Steve / business input)

1. **Rewards mechanics & economics (top priority for Freddie):** Verified externally (Open Standard public materials + Freddie's 8/12 note): yield distributes **to the platform**, not directly to holder wallets — "partners receive direct USD payouts proportional to the OUSD volume they push and hold," Open Standard fee ≤25bps. To confirm: (a) payout currency (USD vs OUSD) and destination (Bridge balance? bank?); (b) cadence; (c) **how Zed's users' self-custody Privy wallets get attributed to Zed's platform** for accrual — registration of addresses? wallets created under Zed's Bridge account?; (d) whether Bridge takes an additional cut on OUSD. Then the business calls: user pass-through share vs. Zed margin, distribution cadence (proposed: accrue daily, pay monthly), minimum balance to earn.
2. **Rate quoting:** How long is an on-ramp quote valid (user sees rate → pays from their bank minutes/hours later)? Proposed: rate locked at deposit-match time, indicative at quote time — simpler treasury, slight UX honesty cost.
3. **Pilot selection:** What criteria pick the 50 (and the wave-1 15)? Power users? High payers? Waitlist volunteers?
4. **Pricing:** FX spread on on/off-ramp (bps)? Flat off-ramp fee or free pilot? (Recommend: modest spread ~50–75bps, no flat fees, so unit economics data is real but adoption isn't suppressed.)
5. **Wallet controls:** Confirm with Privy what controls exist on embedded wallets (transaction policies, allowlists) to harden the UI-enforced closed loop.
6. **Limits:** Confirm/adjust §8 table.
7. **Delinquency policy:** Confirm proposed freeze-on-ramps/allow-off-ramps for delinquent cardholders.
8. **Legal/compliance owner:** Who runs the BSP/counsel track, and what's the drop-dead date for the licensing opinion relative to Phase 2?
9. **Product naming/branding:** What do users see — "Zed Dollars"? "Dollar Account"? How prominently is OUSD/Open Standard disclosed (legal will have a floor; marketing a preference)?
10. **OUSD mechanics to confirm with Bridge in tech design:** exact acquire/redeem API flow (mint/redeem vs. buy/sell), which chains OUSD launches on (Base availability), and whether the $500 test cap can be raised pre-9/15 for internal alpha. (Rewards mechanics moved to #1.)
11. ~~D9/D10 confirmation~~ — resolved in v4 (D9a second VA, D9b Netbank Disburse-to-Account, D10 floats + manual FX, D11 US/EU gated stretch).

---

## 11. Next step

On approval of this PRD (specifically decisions D7–D10 and answers/deferrals on the open questions), produce the **technical design doc**: architecture inside `zed-rust-api`, data model (new tables + shadowledger integration), Bridge (OUSD)/Privy/rails API contracts, treasury automation scope, web app architecture and auth, and an agent-implementable milestone breakdown with per-milestone verification.

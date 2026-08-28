# Zed Dollar Wallet (OUSD) — Product Requirements Document

**Status:** Draft v5.1 — regulatory architecture settled per 8/28 handoff + policy memo; D1–D12 settled; partner/legal confirmations tracked in `counterparty-counsel-tracker.md`
**Date:** 2026-08-28

**Changelog v5 → v5.1:** Processed the two remaining deep-dive artifacts. (1) **`regulatory-policy-memo.md`** (port of the 8/28 positioning memo) is now the authoritative rationale for the v5 architecture — §8 below is rewritten to summarize and reference it instead of restating conclusions without authority (BSP Circular 1206 issuer-offer exclusion, MC/FXD analysis, SEC MC 4/5 CASP risk + relief strategy, StratBox, Howey, EMI). (2) **`counterparty-counsel-tracker.md` replaced** with a faithful port of the authoritative docx tracker from the deep dive (C-BR-1..17, C-PR-1..7, C-NB-1..7, C-LC-1..14, C-INT-1..6, with pilot-blocker vs launch-blocker gates); all PRD references re-anchored to the new IDs. (3) **D10/T2 sharpened:** Netbank is the *preferred* venue for corporate PHP↔USD conversion (C-NB-3/4/6) — confirming the removal of any VASP from the treasury path. (4) **§6.3 sharpened:** Marketing Fee received into a dedicated Zed corporate payout wallet (C-BR-12), assumed paid in OUSD (C-BR-11, working assumption); rewards fulfillment must not be depicted or built as issuer→customer yield. (5) §5 disclosures extended (stablecoin/reserve risk, smart-contract risk, per memo §8).
**Product:** Zed stablecoin store-of-value wallet, piloting on **Open Standard's OUSD** *(working name "Dollar Wallet" — final naming per Open Question #9)*
**Scope:** MVP pilot ("PoC") for 50 of Zed's ~11,000 credit cardholders
**Timeline:** **3–4 week build target** (external launch gated on OUSD public launch, targeted 9/15/26, and on the regulatory gates in R34)

**Changelog v4 → v5:** Regulatory architecture overhaul per Steve's 8/28 handoff memo (`Zed_OUSD_PRD_Agent_Handoff.md`, output of a policy/architecture deep dive), plus three Open Standard program docs (OUSD Rewards, Earning Equity, Supply Contribution Proposal) that answer most of former Open Question #1. The commercial goals and the Bridge + Privy + Netbank counterparties are unchanged; what changed is the *legal characterization of the money flows*: (1) **D4 recast** — on-ramp is **primary issuance**: the customer requests OUSD and pays a PHP amount due; OUSD is minted directly to the customer's wallet; Zed acts as distributor/collection/settlement agent and never creates a customer USD balance (R28). (2) **Zero issuance economics** — no Zed spread or fee on the PHP↔OUSD legs (R29; supersedes T3 and the old pricing question). (3) **D6 recast** — off-ramp is **direct redemption**: the user signs OUSD from their own wallet straight to issuer/Bridge redemption infrastructure; Zed never receives customer OUSD (R30); the "Zed redemption address" is gone. (4) **D3 strengthened / closed-loop abandoned** — the Privy wallet is genuinely user-owned, exportable/recoverable, and **open-loop**; Zed has no unilateral signer or export capability (R31); externally received OUSD shows in the balance truthfully (R32). (5) **D5 recast** — Open Standard's payment is Zed's **Network Partner Marketing Fee** (Zed revenue; mechanics now VERIFIED from OS docs: accrues daily on registered wallets, paid on-chain monthly on the 10th business day); users get a separate **Zed Rewards** program, preferred fulfillment via incremental OUSD mints directly to user wallets. (6) **D10 reworded** — pre-funded Zed-owned USD settlement liquidity + *aggregate own-account* treasury rebalancing; no customer-specific FX; Coins.ph removed from the base architecture (also reflected in D8). (7) **D11 gated on legal** — US/EU off-ramp re-evaluated against BSP M-2026-003 offshore-access rule. (8) New hard requirements **R27–R34**; new **D12** (terminology: no deposit/FX framing). (9) Partner/legal unknowns moved out of §10 into `counterparty-counsel-tracker.md` (Phase 0 artifact); working assumptions about vendor capabilities are explicit gates there, not confirmed facts here. (10) New §2a records Open Standard partner economics (Marketing Fee calc, equity earn-in program, supply attribution) as verified context.

**Changelog v3 → v4:** All remaining architecture decisions settled after code + vendor verification: (1) **D9a** — collections via a *second* per-user Netbank virtual collection account dedicated to stablecoin funding (verified: today's webhook posts every VA credit as a card payment, so purpose-separation must happen at the VA level). (2) **D9b** — payouts via Netbank's Disburse-to-Account API (net-new integration, ~2–4 days; InstaPay < ₱50k real-time, PESONet above; manual bank-portal payout is the fallback runbook, and the Netbank disburse scope/sandbox confirmation is a Phase 0 gate). (3) **D10** — pre-funded floats with *manual* daily FX (dual-controlled) *(superseded in v5 — see D10)*. (4) **D11 (new)** — US/EU off-ramp stays in scope but gated per-user and sequenced as a week-4 stretch. (5) New requirement R12a: destination bank accounts encrypted at rest, masked everywhere, materialized only at disbursement time.

**Changelog v2 → v3:** (1) D7 settled: mobile-responsive web app embedded as a webview tab in the existing native apps, built to graduate to React Native post-MVP. (2) D8 settled: bounded module in `zed-rust-api`, with an explicit caution that the existing Coins.ph USDC code is *reference material*, not a foundation. (3) New hard requirement: lightweight **double-entry ledger over Zed-controlled funds** (§6.8). (4) Yield mechanics corrected after external verification: OUSD yield is distributed **to the platform (Zed), not directly to holder wallets**. (5) Rollout compressed to a 3–4 week build plan.

**Changelog v1 → v2:** Switched from a Zed-branded white-label stablecoin (USDZ) to **OUSD** (Open Standard's stablecoin, accessed via Bridge). Bridge requires a committed minimum mint (typically many millions of dollars) for any white-label coin — not viable for a 50-user PoC. Source: Bridge email thread with Frederick Allen, `Zed - Bridge Email Thread (8.16.26).pdf` in this folder.

---

## 1. Summary

Zed will launch a dollar-denominated store-of-value wallet for Philippine customers, built on **OUSD** (Open Standard's stablecoin, distributed via **Bridge.xyz**), held in **genuinely user-owned, self-custodied embedded wallets powered by Privy**. A user adds dollars by requesting **primary issuance** of OUSD: the app shows the PHP amount due at a transparent reference rate (no Zed spread or fee), the user pays PHP into their dedicated collection account, and OUSD is **minted directly to the user's own wallet**. Zed acts as **distributor, collection agent, and settlement agent** — it funds issuance from its own pre-existing USD liquidity and manages its aggregate currency exposure on its own account. Zed never holds customer OUSD, never creates a customer USD balance, and never executes customer FX.

Users may receive **Zed Rewards** — a Zed-funded, variable rewards program (separate from Open Standard's Network Partner Marketing Fee, which is paid to Zed as revenue) — and can off-ramp at any time: to a Philippine bank account via InstaPay/PESONet (user signs OUSD directly to issuer/Bridge redemption infrastructure; Zed pays PHP locally from its own liquidity), or (gated, pending legal review) to US/EU bank accounts via Bridge's native rails.

**Zed's unique value-add is the PHP leg** — collection, local disbursement, and the distribution relationship. The stablecoin itself, reserve management, mint/redeem infrastructure, US/EU rails, and wallet infrastructure are delegated to Open Standard, Bridge, and Privy.

### Why this product

- PHP has persistently depreciated against USD; middle-class Filipinos want dollar savings but face high minimums, paperwork, and poor rates at traditional banks for USD accounts.
- Zed's cardholders are already KYC'd (Persona), credit-underwritten, and transacting with us — a trusted brand relationship to extend into savings.
- OUSD's Network Partner economics (Marketing Fee ≈ reserve revenue share, §2a) let Zed fund a rewards rate on dollar balances that domestic PHP savings products can't match.
- Strategic: diversifies Zed from mono-line credit into a wallet relationship, increasing retention and lifetime value.

### Why OUSD (not our own coin, yet)

Bridge's white-label issuance requires a contractual minimum mint commitment (many $M). For a 50-user PoC, OUSD gives us the identical product mechanics — primary mint/redeem via Bridge, Marketing Fee economics, multi-chain support — with no mint commitment. Branding is the trade-off: the token is OUSD, and the *wallet experience* is Zed's (see Open Question #9 on product naming). White-label becomes a scale-up decision if the PoC succeeds (§2a's equity program economics — $50M minimum supply — are also only relevant at scale).

### External timeline constraints (from Bridge, as of 8/14/26)

- OUSD is **live for testing now, capped at $500 total for Zed** (entity-level cap, not per end user; testing means Zed testing, not Zed's users).
- Open Standard targets **9/15/2026 for public OUSD launch** — external pilot users cannot be funded at real size before then.
- Open Standard dashboard **API key available Sept 2026**; wallet registration accrual is **not backdated**, so wallets must be registered as they are created (§2a, §6.3).

---

## 2. Goals & success metrics (pilot)

| Goal | Metric | Target |
|---|---|---|
| Validate demand | Pilot users who complete ≥1 on-ramp | ≥ 35 of 50 (70%) |
| Validate store-of-value behavior | 30-day balance retention (balances held, not immediately off-ramped) | ≥ 60% of deposited value retained at day 30 |
| Validate repeat usage | Users with ≥2 on-ramps in first 60 days | ≥ 40% |
| Operational soundness | On-ramp PHP received → OUSD minted to wallet, median time | ≤ 30 min during business hours *(proposed)* |
| Operational soundness | PH off-ramp request → PHP received median time | ≤ 1 business day *(proposed)* |
| Zero-loss bar | Reconciliation breaks unresolved > 24h; user funds lost | 0 |
| Rewards work | Zed Rewards accrue and post correctly for 100% of eligible holders | 100% |

Secondary learning goals: real rails cost per transaction, treasury liquidity sizing, support ticket volume/themes, demand for US/EU off-ramp, realized Marketing Fee revenue vs. Zed Rewards cost (validates program economics and the white-label decision at the scale-up gate).

### 2a. Open Standard partner economics *(added v5 — VERIFIED from OS program docs, 8/28; commercial terms governed by the OS agreement)*

Context for D5, §6.3, and the scale-up gate. Three OS documents received 8/28:

- **Marketing Fee (OUSD Rewards doc):** OUSD reserve revenue (cash + short-term treasuries, held via OS's issuing partner) is distributed monthly to Network Partners in proportion to OUSD held across their **registered wallets**, paid as a **Marketing Fee**. Accrues daily (daily balance × daily net yield, balances sampled at unannounced times); paid **on the 10th business day** of the following month, **on-chain to a payout wallet the partner designates** (payout token to confirm — tracker C-BR-11/12). Wallets qualify by **Ownership** (partner controls the wallet) or **Relationship** (wallet provisioned for / custodying OUSD for a direct customer with an active relationship) — Zed-provisioned user-owned Privy wallets are the Relationship case (attribution construct only; tracker C-BR-6/17). Registration via dashboard/API/CSV; **unregistered wallets do not accrue and accrual is not backdated**. Illustrative net yield in OS's examples: 3.75%/yr.
- **Equity earn-in (Earning Equity doc):** partners can buy into OS equity annually pro-rata to **Ecosystem Activity** = Supply (average daily OUSD balance across registered wallets) + Qualified Flow (5% of OUSD moved with other partners' registered wallets, capped at 1.5× Supply; intra-platform, unregistered, and round-trip flow excluded). Pool: 10%/yr for the first four years (40% total); 5% max ownership per partner group; **$50M minimum supply to qualify** — far beyond pilot scale, relevant only to the scale-up decision gate.
- **Supply attribution (Supply Contribution Proposal):** token-level "coloring" — OUSD picks up a partner's color when it lands in a registered address and the color travels with the token; exits from unclaimed addresses draw own-color first, then weighted-random. Implication for Zed: register every wallet tied to the platform promptly (Phase 0 action), and expect attribution to be measurable by OS independent of our books.

---

## 3. Non-goals (explicitly out of MVP)

1. **Payments / spend from OUSD** — no card funding, bill pay, P2P transfers, or merchant payments from the balance. Store of value only.
2. **External send/receive UI** *(rewritten in v5 — was "external crypto transfers" prohibition)* — MVP ships without in-app external send/receive, but the wallet is **open-loop** (D3): externally received OUSD is recognized in the displayed balance (R32), the user can export/recover the wallet and use it independently of Zed, and in-app send/receive is on the product roadmap (all sends user-signed, R31). The old "closed-loop, ignore unsolicited deposits" posture is retired.
3. **Non-cardholders** — pilot is invite-only from the existing cardholder base.
4. **Other stablecoins/assets** — OUSD only. No USDC/USDT balances shown, no trading.
5. **Scale** — 50 users. Manual/semi-manual ops steps are acceptable where they buy speed to launch (documented in runbooks).
6. **Native mobile UI** — MVP ships as a web app (Decision D7). Native iOS/Android integration comes post-validation.
7. **Paying the Zed card bill from the balance** — natural follow-on, deliberately excluded from MVP to keep the money surface minimal.
8. **White-label stablecoin** — deferred to the post-pilot decision gate.

---

## 4. Decisions

### Settled (per Steve / Bridge thread; v5 revisions per 8/28 handoff)

| # | Decision | Choice |
|---|---|---|
| D1 | Product core | Store of value: hold OUSD, earn Zed Rewards, on/off-ramp. No spend. |
| D2 | Stablecoin | **OUSD** (Open Standard), accessed via **Bridge.xyz**. White-label revisited post-pilot. |
| D3 | Custody *(revised v5)* | **Genuinely user-owned self-custody** via **Privy** embedded wallets: the user is the wallet owner; recovery/export path lets the user use the wallet independently of Zed; **no Zed authorization key, signer, owner role, or export capability** (R31); **open-loop** (R32). No seed-phrase UX. Privy configuration confirmation is a Phase 0 gate (tracker C-PR-1..5). |
| D4 | On-ramp *(revised v5)* | **Primary issuance, Zed as distributor/collection/settlement agent**: user requests OUSD; app shows PHP amount due at a transparent reference rate with **zero Zed spread/fee** (R29); PHP collected via the dedicated Netbank VA is issuance consideration; Zed funds issuance from **pre-existing Zed-owned USD liquidity** at Bridge; **OUSD is minted directly to the user's Privy address** (R27) — no Zed OUSD inventory/resale, no customer USD balance at any point (R28). Full flow in §6.2. |
| D5 | Rewards *(revised v5)* | Two separate things: (a) **Open Standard pays Zed a Network Partner Marketing Fee** (mechanics VERIFIED, §2a) — booked as **Zed revenue** (accounting confirmation: tracker C-INT-6), received into a dedicated Zed corporate payout wallet (C-BR-12; payout asset assumed OUSD — C-BR-11), not customer property; (b) **"Zed Rewards"** — a Zed-funded, variable-rate rewards program for users with its own terms and accrual logic (§6.3). Preferred fulfillment: **incremental OUSD primary mints directly to user wallets** (tracker C-BR-13); Zed payout-wallet → user-wallet transfer is the fallback, requiring legal sign-off. Never marketed as interest or as the user owning OS's fee. |
| D6 | Off-ramp *(revised v5)* | PH: **direct redemption** — user signs OUSD from their own wallet **directly to issuer/Bridge redemption infrastructure** via a customer-attributed redemption route; **Zed never receives customer OUSD** (R30); USD proceeds settle to Zed's settlement balance, operation-attributed; Zed pays PHP locally via Netbank Disburse-to-Account (§6.4). US/EU via Bridge rails per D11. If Bridge cannot support the direct pattern, **do not** fall back to customer→Zed-wallet — escalate (fallback decision: licensed PH VASP off-ramp, or defer PH off-ramp). Phase 0 gates: tracker C-BR-7..10. |
| D6a | KYC | Reuse existing **Persona** KYC; share data with Bridge so pilot users don't re-KYC. |
| D6b | Chain | EVM L2 preferred, **Base** the leading candidate. Confirm OUSD's default/supported chains with Bridge in tech design (tracker C-BR-16). |

### Settled in v3 (per Steve, 8/16)

| # | Decision | Choice | Notes |
|---|---|---|---|
| D7 | Client surface | **Mobile-responsive web app, embedded as a webview tab inside the existing native apps.** Built in React with React-Native-portable patterns so it can graduate to an in-app React Native section post-MVP. | Session hand-off from the native app to the webview is a first-class tech-design item. Web deploys iterate daily with no app-store cycle during the pilot. |
| D8 | Backend home *(revised v5)* | **New bounded module inside `zed-rust-api`** (own tables, own route namespace, feature-flagged; no foreign keys into card tables beyond `user_id`). | Reuses auth/sessions, users table, Persona artifacts, deploy/CI/workers, incoming-payments matching, QRPH collections. **Coins.ph is removed from the base architecture** (v5): the existing Coins.ph USDC code is reference material only, and Coins.ph is **not** an expected customer-path or treasury venue — retain at most an optional, clearly-isolated fallback adapter if later required as a regulated venue. The OUSD module owns its own money tracking (§6.8). |

### Settled in v4 (per Steve + code/vendor verification, 8/16)

| # | Decision | Choice | Rationale |
|---|---|---|---|
| D9a | PHP collections | **Second per-user Netbank virtual collection account, dedicated to stablecoin funding.** Verified in code: each user already gets a Netbank VA with QRPH generated against it, and the webhook posts *every* credit to it as a card payment. A second, purpose-dedicated VA per user cleanly separates card bill-pay from Dollar Wallet funding. | Reuses the live, proven collection rail these exact users already use; the only change is a purpose dimension on VA issuance and a branch in the webhook. |
| D9b | PHP payouts | **Netbank Disburse-to-Account API in MVP** (net-new integration). Single endpoint; real-time InstaPay < ₱50k; PESONet for larger. Same vendor and auth pattern as collections; sized ~2–4 days incl. payout state machine. **Manual bank-portal payout with dual approval is the documented fallback runbook.** Phase 0 gate: confirm disburse scope + sandbox credentials (tracker C-NB-5). | One vendor for both PHP legs. If the capability check fails or slips, fall back to manual payouts for wave 1 without changing user-facing flow. |
| D10 | Treasury *(revised v5)* | **Pre-funded Zed-owned liquidity + aggregate own-account rebalancing.** USD settlement liquidity at Bridge (Zed's own funds, consumed by issuance and replenished by redemptions); PHP liquidity at Netbank. Ramps execute instantly against Zed's own balances. Treasury periodically converts **aggregate** Zed-owned PHP↔USD on its own account — **Netbank preferred as the executing bank** (corporate conversion + USD funding to Bridge: tracker C-NB-3/4/6), manual, dual-controlled — **never a customer-specific trade, never a customer FX service**. Coins.ph is not in the money path (D8; per memo §4, no VASP is inserted into treasury). Automation is a post-MVP upgrade. | Instant-feeling UX; currency exposure bounded and trivial at pilot caps; own-account framing keeps Zed out of the customer-FX business — the point of the v5 architecture. |
| D11 | US/EU off-ramp *(revised v5)* | **In scope, gated per-user, sequenced after PH flows are green (week-4 stretch), and additionally gated on legal review of BSP M-2026-003** (offshore-access rule): Bridge must remain **Zed's counterparty**, never a direct retail interface for PH users (R33; tracker C-LC-3). Only destinations with existing Bridge fiat off-ramps. | The redemption leg exists regardless; the US/EU leg is external-account registration + a Bridge transfer. The legal gate decides whether it ships at all. |

### Settled in v5 (per 8/28 handoff)

| # | Decision | Choice | Rationale |
|---|---|---|---|
| D12 | Product terminology | **"OUSD Wallet" / "Dollar Wallet"** framing (final name: Open Question #9). Prohibited without compliance sign-off: "deposit," "savings account," "interest," "convert PHP to USD," "FX spread," "USD balance," "Zed holds your dollars," "closed loop," "Zed redemption address," "OUSD earns Treasury yield." Required framings: "Add OUSD" / "request OUSD issuance"; "PHP amount due at a transparent reference rate"; "OUSD balance"; "your OUSD is held in your self-custodied wallet"; "open-loop self-custodied wallet"; "issuer/Bridge redemption route"; "eligible OUSD may receive variable Zed Rewards." | Terminology is load-bearing for the regulatory characterization: the product is distribution of a third-party stablecoin, not deposit-taking, not FX, not custody. |

---

## 5. Users & eligibility

- **Pilot cohort:** 50 users, invite-only, selected from the ~11,000 active cardholders.
- **Proposed eligibility criteria** *(confirm — Open Question #3)*: account in good standing (not delinquent), Persona KYC completed at a tier sufficient for Bridge's requirements, active app usage in the last 90 days, and opt-in via waitlist/invitation.
- Users must accept new terms: Zed Dollar Wallet terms of service, Zed Rewards program terms (separate, per D5), Bridge's end-user terms, applicable OUSD/Open Standard terms, and Privy's terms, with clear self-custody and no-deposit-insurance disclosures (this is not a bank deposit; not PDIC-insured; OUSD is issued by Open Standard, not Zed; the wallet is user-owned and exportable; stablecoin/reserve and smart-contract/blockchain risks disclosed per memo §8).
- If a pilot user becomes delinquent on their card, their OUSD remains theirs (self-custody — Zed cannot seize it, and per R31 could not move it even operationally). Proposed policy: freeze *new on-ramps* for delinquent users; off-ramp remains available. *(Confirm — Open Question #7.)*

---

## 6. Product requirements

### 6.1 Onboarding / account opening

1. Invited user opens the web app and authenticates with their existing Zed credentials (same auth as the mobile apps, via zed-rust-api).
2. User reviews and accepts terms and self-custody + risk disclosures (including the open-loop nature of the wallet and the recovery/export path).
3. Behind the scenes, Zed:
   - Creates a **Bridge customer** using shared Persona KYC data. If Bridge requires additional fields, the user completes only the delta.
   - Provisions a **user-owned Privy embedded wallet** per D3 (user is owner; recovery/export available; no Zed signer — configuration per tracker C-PR-1..5).
   - Registers the wallet address with the account module **and with Open Standard's wallet registry** (accrual is not backdated — §2a).
4. User lands on a zero-balance home screen with a clear "Add dollars" call to action.

**Requirements:**
- R1. Onboarding must complete in a single session, < 5 minutes for a user whose Persona KYC transfers cleanly.
- R2. If Bridge KYC fails or needs review, the user sees a "we're reviewing your account" state; ops is alerted (Slack), and the user is notified when resolved.
- R3. All consents (terms versions, timestamps) are recorded per user.

### 6.2 On-ramp — primary issuance (PHP consideration → OUSD minted to user) *(rewritten v5)*

1. **Quote/request.** User selects the amount of OUSD to add (e.g., 100 OUSD). Zed shows the PHP amount due using a transparent reference rate and **zero Zed issuance/FX fee** (R29). Reference-rate validity window per Open Question #2.
2. **PHP collection.** User pays from their own bank/e-wallet via QRPH or transfer to their **stablecoin-dedicated Netbank virtual account** (D9a). Zed's incoming-payments pipeline detects and matches the deposit; the dedicated VA makes funding intent unambiguous.
3. **Issuance funding.** On match, Zed consumes **pre-existing Zed-owned USD liquidity** in the Bridge settlement/prefunded arrangement. **No user USD balance or customer-specific USD entitlement is created** (R28).
4. **Primary mint.** Bridge/OUSD issuance infrastructure **mints OUSD directly to the customer's Privy address** (R27). Record the issuer/Bridge transaction ID and on-chain mint hash.
5. User sees pending → completed states, push/email notification on completion, and the mint in their activity feed.
6. **Treasury rebalance (separate).** Ops/treasury periodically converts aggregate Zed-owned PHP into USD to replenish the settlement balance (D10) — decoupled from any customer operation.

**Requirements:**
- R4. Median PHP-received-to-mint ≤ 30 min during business hours; hard SLA of same business day. Deposits outside business hours process next window *(if liquidity permits 24/7, better — tech design decides)*.
- R5. Unmatched or out-of-limit deposits alert ops within 15 minutes; refund-to-source is the documented default remedy.
- R6 *(revised v5)*. Every on-ramp records: PHP consideration received, reference rate shown, Zed USD settlement asset consumed, issuer/Bridge transaction ID, OUSD minted, on-chain mint hash — reconcilable end to end in the ledger. (Replaces the old per-operation "customer PHP → customer USD" fields.)
- R7. Limits enforced at quote time and at match time (per-user and pilot-wide caps, §8).

### 6.3 Holding & Zed Rewards *(rewritten v5)*

1. Home screen shows: OUSD balance (from chain), PHP-equivalent at current indicative reference rate, lifetime Zed Rewards earned, and the current Zed Rewards rate — clearly labeled **"variable Zed Rewards,"** never "interest" or a guaranteed APY (D12, R10).
2. **Program structure (per D5):** Open Standard pays Zed a Network Partner Marketing Fee on OUSD held in registered wallets (mechanics §2a — accrues daily, paid on-chain monthly on the 10th business day). This is Zed revenue. Separately, **Zed Rewards** accrue to users under Zed's own program terms (proposed: accrue daily on on-chain balances, distribute monthly), at a rate Zed sets and can vary.
3. **Fulfillment:** preferred — Zed funds **incremental OUSD primary mints directly to user wallets** (tracker C-BR-13); fallback — transfers from a Zed payout wallet, only with legal sign-off. The Marketing Fee itself is received into a **dedicated Zed corporate payout wallet** (C-BR-12), kept strictly separate from customer assets; the fee is never depicted or built as issuer→customer yield.
4. **Wallet registration:** every user wallet is registered with Open Standard at creation (§6.1) so Marketing Fee accrual matches the user base; registration uses the Relationship qualification (§2a; attribution construct only, under Zed's relationship — tracker C-BR-6/C-BR-17).
5. Activity feed shows every event: mints (on-ramps), redemptions (off-ramps), Zed Rewards distributions.

**Requirements:**
- R8 *(revised v5)*. Zed Rewards math is deterministic and auditable: each distribution records the balance snapshot(s), rate, period, and resulting OUSD amount per user; program cost reconciles against Marketing Fee revenue actually received for the period (they are related but **not** contractually coupled — the reconciliation is economic, not a pass-through claim).
- R8a. User-balance snapshots for accrual are taken from on-chain wallet balances (source of truth), not from an internal running balance.
- R9 *(revised v5)*. The displayed rate is the Zed Rewards rate — set by Zed, informed by (not defined as) Marketing Fee economics (OS fee ≤ 25bps of yield per the 8/12 thread; realized net yield visible in §2a mechanics). Rate changes are versioned and displayed prospectively.
- R10. Marketing/UX language must not call rewards "interest" or the product a "deposit/savings account" (D12); program terms must not state that the customer owns Open Standard's Marketing Fee.

### 6.4 Off-ramp — Philippine bank via direct redemption *(rewritten v5)*

1. User taps "Withdraw," chooses "Philippine bank account," enters/selects a destination account, and an amount within limits. Zed shows estimated PHP proceeds and any disclosed local rail fee — **not** framed as Zed buying OUSD or converting currency (D12).
2. **Customer-attributed redemption route.** Zed creates/uses a Bridge redemption route tied to the Bridge customer / `on_behalf_of` identifier (or a customer-specific liquidation address) — tracker C-BR-7/C-BR-8/C-BR-9.
3. **User signs OUSD directly to the redemption infrastructure** (Privy signing UX). Source: the customer's wallet. Destination: **issuer/Bridge infrastructure — never a Zed wallet** (R30).
4. **Redemption/burn.** Bridge/OUSD issuer redeems; USD proceeds settle into Zed's settlement/prefunded arrangement, attributable to the specific redemption operation.
5. **Local payout.** Zed pays PHP from its own PHP liquidity via the **Netbank Disburse-to-Account API** (D9b: InstaPay < ₱50k real-time, PESONet above; manual bank-portal payout with dual approval is the fallback runbook).
6. States: requested → redemption signed → redeemed → PHP sent → completed, with notifications. Failures (bad account number, rail rejection) surface to the user with ops alerting.
7. **Treasury rebalances separately** (D10) — no customer-specific USD/PHP trade is ever booked.

**Requirements:**
- R12a. **Destination account storage:** account numbers encrypted at rest (app-level), rendered masked everywhere (UI, logs, Slack alerts, ops dashboard), full value materialized only at disbursement call time. Account holder name + bank code stored alongside for name-match checks.
- R11. Median request-to-PHP-received ≤ 1 business day; InstaPay-eligible amounts (≤ ₱50k) should typically land same day.
- R12. First off-ramp to a new destination account may require a verification step (proposed: micro-confirmation of account-holder name match where the rail returns it).
- R13. Destination account holder must be the user themselves for MVP (name-match policy; third-party payouts excluded).
- R14 *(revised v5)*. Every off-ramp records: OUSD signed to redemption (tx hash), redemption/burn reference, USD settled to Zed (operation-attributed), PHP paid, rail used, rail reference — ledger-reconcilable end to end.

### 6.5 Off-ramp — US/EU bank (via Bridge) *(revised v5)*

1. Same entry point; user selects "US bank (USD)" or "EU bank (EUR/SEPA)," provides account details; after direct redemption (as §6.4 steps 2–4), Bridge pays out via its native fiat rails.
2. Zed passes through Bridge's rails, fees, and timelines transparently.

**Requirements:**
- R15 *(revised v5)*. Gated per-user behind "contact support to enable"; built as a week-4 stretch after PH flows are green; **and gated on legal review of BSP M-2026-003** — Bridge remains Zed's counterparty and is never presented as a direct retail app/interface to PH users (R33; tracker C-LC-5). Only destinations with existing Bridge fiat off-ramps are offered.
- R13 (name-match: user's own account) and R12a (encrypted storage, masked rendering) apply here too.

### 6.6 Notifications & comms

- R16. Transactional notifications (email + push via existing channels) for: onboarding approved, deposit received, OUSD minted, withdrawal stages, Zed Rewards posted.
- R17. A pilot-support channel (existing in-app support / concierge Slack-backed flow) with a dedicated runbook for account issues.

### 6.7 Ops & internal tooling

- R18. **Ops dashboard** (internal, can be minimal/admin-grade): pending on-ramps and off-ramps with state, unmatched deposits, liquidity balances (PHP, USD settlement at Bridge, Zed Rewards funding), manual retry/resolve actions with audit log.
- R19. **Dual control** on any manual money movement (treasury rebalance, manual disbursement, refund): initiated by one operator, approved by a second. At pilot scale this can be a Slack-approval flow, but it must exist from day one.
- R20. **Daily reconciliation** job + report: internal ledger vs. Bridge balances vs. on-chain OUSD per wallet vs. bank/rail statements. Any break pages ops; unresolved > 24h breaches the pilot's zero-loss bar (§2).
- R21. **Runbooks** written before launch: stuck on-ramp, stuck off-ramp, Bridge outage, Privy outage, rail outage, user-reported missing funds, pilot halt procedure ("close the ramp": disable on-ramps while keeping off-ramps working).

### 6.8 Money tracking & ledger *(v3 hard requirement; account model revised v5)*

The zero-loss bar (§2) is enforced by construction, not by hope.

- R22 *(revised v5)*. **Lightweight double-entry ledger over Zed-controlled funds.** Accounts (indicative, per the issuance/redemption model): PHP liquidity; USD settlement asset at Bridge; PHP-consideration-in-flight (deposit matched, mint not yet confirmed); redemption-in-flight (OUSD signed to redemption, PHP not yet paid); Marketing Fee revenue; Zed Rewards accrued (program liability); treasury rebalance clearing. Every on-ramp, off-ramp, treasury rebalance, Marketing Fee receipt, and Zed Rewards event posts balanced entries; the ledger is append-only. (Replaces the v4 account list built on per-customer FX concepts.)
- R23. **User balances are NOT ledger liabilities.** Users self-custody OUSD; the chain is the source of truth for user balances. The ledger tracks only money Zed controls or is mid-flight on. Reinforced by R28: no ledger or database object may represent a customer USD entitlement.
- R24. **Per-operation state machines** with an immutable event trail for every ramp (per R6/R14); no operation can silently disappear — terminal states are only `completed`, `refunded`, or `failed-with-ops-resolution`.
- R25. **Daily reconciliation ties the three worlds together** (extends R20): ledger balances vs. Bridge/bank statements vs. on-chain OUSD across user wallets (expected-from-operations vs. actual). Any drift is a paged break.
- R26. The existing `shadowledger` service is **evaluated, not assumed**, in tech design: reuse it only if its posting model fits cleanly; if it is card-domain-tied, build standalone tables for this module.

### 6.9 Regulatory architecture invariants *(added v5 — hard requirements from the 8/28 handoff)*

- **R27 — Primary issuance.** Customer on-ramps must settle as a primary OUSD mint directly to the customer wallet; no Zed inventory resale without legal approval.
- **R28 — No customer USD.** No database or ledger object may represent a customer USD entitlement or balance.
- **R29 — Zero issuance economics.** Zed charges no spread or fee on PHP-to-OUSD issuance for the pilot. (Supersedes T3.)
- **R30 — No Zed custody.** No customer OUSD may be held in a Zed-controlled wallet at any time, including during on-ramp or redemption.
- **R31 — User signing.** All outbound wallet transactions require user cryptographic authorization; Zed cannot unilaterally sign, change owners/signers/policies, or export keys.
- **R32 — Open-loop truthfulness.** External OUSD received by the wallet is recognized in the displayed on-chain balance; compliance controls may block in-app actions but must not falsify ownership or balances.
- **R33 — Counterparty attribution.** Each mint/redemption is attributable to a Zed user in Bridge/OUSD systems (customer / `on_behalf_of` records) without giving that user direct retail access to an offshore VASP interface.
- **R34 — Regulatory gates.** External launch requires written sign-off on BSP VASP/FX posture and a resolved SEC path: no-action/interpretive confirmation, exemption, or StratBox relief. (Tracker C-LC-1..14; strategy per `regulatory-policy-memo.md` §5/§10.)

---

## 7. Treasury requirements (per D10, revised v5)

- T1 *(revised v5)*. USD settlement liquidity pre-funded at Bridge from **Zed-owned funds**, sized to ≥ 1 typical day of issuance (initial proposal: $25k, revisit weekly); PHP liquidity at Netbank sized to ≥ 2 typical days of off-ramps (initial proposal: ₱1.5M).
- T2 *(revised v5)*. Periodic **aggregate own-account rebalancing**: net Zed-owned PHP converted to USD and vice versa via a partner bank/FI, executed manually, dual-controlled, recorded in the ledger. **Never a customer-specific trade** — customer operations only ever touch Zed's pre-existing balances. Coins.ph is not a venue (D8); automation is post-MVP.
- ~~T3~~ *(superseded v5 by R29 — zero customer issuance economics; no spread configuration exists. Reference-rate sourcing and display are defined in tech design.)*
- T4. Liquidity thresholds alert ops (Slack) when below 0.5 days of expected volume; issuance quoting pauses gracefully ("adds temporarily delayed") if the USD settlement balance cannot cover pending mints.
- T5 *(revised v5)*. Weekly treasury report: liquidity levels, rebalancing cost, Marketing Fee received vs. Zed Rewards accrued/distributed.

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

**Compliance posture (v5.1 — authority: `regulatory-policy-memo.md`; confirmations: tracker §4; gates: R34):**
- **Executive position (memo):** strong basis that Zed needs **no BSP VASP or money-changing/FX authority**; the remaining material perimeter is the **SEC CASP regime** (Zed may be an "offeror"/intermediary under MC 4, s. 2025 even without operating an exchange). Strategy: SEC interpretive confirmation first, then MC 5 registration exemption, StratBox (MC 9, s. 2024) as pilot fallback — not a full CASP license build.
- **BSP VASP thesis (memo §3):** the M-Regulations (Circular 1206) exclude services related to an *issuer's offer/sale* and entities acting *solely on their own behalf*. The architecture is built on those two exclusions — genuine primary issuance (no Zed inventory, no secondary execution, no spread: R27/R29), direct issuer redemption (R30), no custody/control (R31), own-account treasury (D10). The per-limb analysis (fiat↔VA, VA↔VA, transfer, safekeeping) is in the memo; counsel confirmation is C-LC-1..4.
- **Core design principle (memo §1):** every regulated-looking function must be issuer activity, Zed own-account treasury, bank activity, or customer-controlled wallet activity. The memo's §9 "facts to avoid" table (customer USD entitlements, Zed spread, Zed inventory, customer OUSD to Zed, omnibus wallet, Zed signer, intermediate USDC, yield language) is binding on product and engineering — mirrored in R27–R32 and D12.
- **Offshore counterparty (memo §3.2, BSP M-2026-003):** Bridge is Zed's infrastructure/counterparty, never a retail interface for PH users; Bridge customer/`on_behalf_of` records are KYC/attribution constructs (R33, C-LC-5, C-BR-6); Bridge home-jurisdiction licensing evidence is launch diligence (C-BR-14).
- **Securities overlay (memo §6):** working position OUSD is not itself a security (1:1 redemption, no token-level yield right — C-LC-10), and the separate, discretionary Zed Rewards program must not create one (C-LC-11). This is *why* D5's Marketing-Fee/Zed-Rewards separation exists.
- **EMI/deposit-taking (memo §7):** no Zed monetary-value liability exists — the customer's asset is issuer-issued OUSD on-chain (C-LC-12). D12 terminology enforces the characterization.
- **Open-loop posture** *(replaces v4 closed-loop rationale)*: the wallet is user-owned and externally usable (D3, R31, R32). Compliance controls operate on *Zed's product actions* — ramp screening, in-app action gating, monitoring of registered wallets — never by falsifying balances. Wallet screening policy (external inbound/outbound, sanctions, unsupported assets) is C-INT-4; whether user-signed send/receive UI creates a residual VASP "transfer" limb is C-LC-2.
- Own-account-only fiat legs (R13) keep AML/travel-rule surface minimal for MVP; existing monitoring obligations extend to this product (Comply Advantage where applicable), with crypto indicators added to monitoring/case-management rules and AMLC posture confirmed (C-LC-13/14).
- Clear user disclosures (memo §8): not a bank deposit, not PDIC-insured, variable Zed Rewards (not interest), FX risk on the PHP value of holdings, self-custody model with export/recovery, OUSD issued by Open Standard, stablecoin/reserve risk, smart-contract/blockchain risk.

**Key product risks:**

| Risk | Mitigation |
|---|---|
| Regulatory: PHP↔OUSD activity deemed licensable (BSP VASP/FX) or an unregistered offering (SEC) | Counsel review pre-launch = R34 launch gate; distributor/agent architecture (R27–R33); 50-user invite-only framing; StratBox/no-action paths scoped |
| Bridge cannot support direct mint-to-wallet or direct redemption (working assumptions, §tracker) | Phase 0 confirmation gates C-BR-2/3 and C-BR-7..10; if unsupported, escalate to fallback decision (licensed PH VASP off-ramp or defer) — never customer→Zed-wallet |
| OUSD/Open Standard dependency (launch slips past 9/15; depeg or reserve issues) | Timeline buffer; monitor via Bridge; off-ramp-priority halt procedure; scale-up gate re-evaluates issuer choice |
| Currency exposure on Zed's own liquidity | Caps + periodic aggregate rebalancing + small liquidity sizing (T1–T4) |
| Reconciliation break / lost funds | Ledger-first design, daily recon (R20/R25), dual control (R19), zero-loss bar |
| Bridge or Privy outage/dependency | Runbooks (R21); "close the ramp" procedure; off-ramp-priority recovery |
| User confusion about self-custody / recovery | Privy recovery/export UX + onboarding education screen; pilot concierge support |
| Open-loop misuse (external transfers to/from user wallets) | Screening + monitoring on registered wallets; in-app action gating (R32 boundaries); own-account fiat legs; pilot scale |
| Rewards mislabeled as interest → regulatory exposure | D12 terminology + R10 language review; separate Zed Rewards terms |

---

## 9. Rollout plan — 3–4 week build

Anchors: build starts **week of 8/18**; Open Standard's public OUSD launch targeted **9/15/2026**. External users are gated on the later of build-complete, OUSD launch, and the R34 regulatory gates.

**Phase 0 — Partner & legal track (immediately, parallel to build):** tracked item-by-item in `counterparty-counsel-tracker.md`. Headlines:
- Complete **Bridge KYB** (owner: Steve — gates OUSD test access; funds-flow doc prepared 8/27).
- **Bridge / Open Standard:** legal issuer of record; primary mint direct-to-customer-wallet; direct redemption + settlement attribution; retail-relationship structure; Marketing Fee asset/wallet; reward minting; home-jurisdiction licensing; chains + test-cap; immediate wallet registration (C-BR-1..17).
- **Privy:** contract + sandbox; user-sole-owner configuration, no Zed signer, export/recovery, open-loop send/receive, direct redemption signing, non-custodial policy controls (C-PR-1..7).
- **Netbank:** second VA per user; collections documented as purpose-specific settlement; corporate PHP↔USD conversion + USD funding to Bridge; Disburse-to-Account scope/sandbox; account segregation (C-NB-1..7).
- **Counsel:** BSP issuer-offer exclusion, transfer-limb, redemption treatment, FX posture, M-2026-003; SEC CASP classification/exemption/offering/StratBox; security analysis; EMI; disclosures; AMLC (C-LC-1..14) — the R34 gates.
- **Internal:** naming, reference-rate policy, rewards formula, wallet screening policy, regulatory engagement sequence, accounting treatment (C-INT-1..6).

**Week 1 (8/18) — Foundations:** backend module skeleton (tables, ledger per §6.8, operation state machines, feature flag), Bridge + Privy sandbox clients, web app skeleton with auth/session hand-off, onboarding flow against sandbox.
**Week 2 (8/25) — Money flows:** on-ramp end-to-end in sandbox (QRPH/reference deposit → match → primary mint to wallet), off-ramp end-to-end (direct redemption → InstaPay/PESONet payout), reconciliation job v1, minimal ops dashboard + dual-control approvals.
**Week 3 (9/1) — Hardening + internal alpha:** Zed Rewards accrual/distribution job, notifications, runbooks, real-money internal alpha under the **$500 entity-wide test cap**, daily recon running clean.
**Week 4 (9/8–9/15) — Polish + launch readiness:** alpha fixes, limits enforcement verified, counsel/compliance check-in against R34, wave-1 user selection and comms prepared. **At OUSD public launch (≈9/15) + R34 sign-off: Phase 2.**

**Phase 2 — Pilot wave 1:** 15 external users at real limits. Exit: ≥ 10 funded accounts, no unresolved recon breaks, support load acceptable.
**Phase 3 — Full pilot:** all 50 users. Runs ≥ 60 days against §2 metrics.
**Decision gate:** scale (React Native in-app section, higher caps, more users, **white-label vs. staying on OUSD** — informed by §2a equity economics at realized AUM), pivot, or wind down (wind-down = off-ramp everyone, a first-class documented flow).

Timeline risks: KYB/partner-access delays directly eat build weeks; the Bridge direct-mint/redeem confirmations (C-BR-2/3, C-BR-7..10) now sit on the critical path of the *architecture*, not just access; OUSD public launch slipping delays wave 1 but not the build; counsel (R34) is the item that can block launch with the build finished.

---

## 10. Open questions (business — Steve's calls)

*Partner-capability and legal confirmations moved to `counterparty-counsel-tracker.md` (v5); this section is now business decisions only.*

1. **Zed Rewards economics** *(reframed v5 — mechanics now verified, §2a; = tracker C-INT-3)*: set the Zed Rewards rate (vs. realized Marketing Fee revenue), distribution cadence (proposed: accrue daily, pay monthly), minimum balance to earn (if any), and whether the rate is published as a number or a range. (Partner-mechanics sub-questions → tracker C-BR-11/12/17.)
2. **Reference-rate policy** *(= tracker C-INT-2)*: which reference rate is displayed, and how long is a quote's PHP-amount-due valid (user sees amount → pays from their bank minutes/hours later)? Proposed: amount fixed at quote time within a validity window; tech design defines the stale-quote remedy (top-up request vs. partial mint vs. refund).
3. **Pilot selection:** what criteria pick the 50 (and the wave-1 15)? Power users? High payers? Waitlist volunteers?
4. ~~Pricing~~ *(superseded v5 by R29 — zero spread/fee for the pilot. Post-pilot monetization is a scale-up-gate question.)*
5. **Recovery/export UX:** how prominently is wallet export/recovery surfaced (it must exist per D3; the question is UX placement and support burden)? (Privy capability confirmation → tracker C-PR-3/C-PR-7.)
6. **Limits:** confirm/adjust §8 table.
7. **Delinquency policy:** confirm proposed freeze-on-ramps/allow-off-ramps for delinquent cardholders.
8. **Legal/compliance owner:** who runs the BSP + SEC counsel track (R34), and what's the drop-dead date for the opinions relative to Phase 2? Includes the engagement-sequence call (tracker C-INT-5: informal meeting vs. written interpretive request vs. exemption vs. StratBox first).
9. **Product naming/branding** *(= tracker C-INT-1)*: "Dollar Wallet"? "OUSD Wallet"? How prominently is OUSD/Open Standard disclosed (legal floor; marketing preference). D12 constrains the vocabulary either way.
10. ~~OUSD mechanics to confirm with Bridge~~ *(moved v5 → tracker C-BR-1..17)*
11. ~~D9/D10 confirmation~~ — resolved in v4.

---

## 11. Next step

On approval of this PRD (specifically the v5 architecture: D3/D4/D5/D6/D10–D12 and R27–R34), produce the **technical design doc**: architecture inside `zed-rust-api`, data model (new tables + §6.8 ledger), Bridge issuance/redemption and Privy API contracts (with each tracker working-assumption mapped to a `PENDING` section), Netbank collection/disbursement integration, Open Standard wallet-registration integration, web app architecture and auth, and an agent-implementable milestone breakdown with per-milestone verification.

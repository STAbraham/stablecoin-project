# Zed Dollar Wallet — Modular PRD (wallet-first)

**Status:** Draft v0.5 (2026-11-27) — settled facts only; decisions marked `OPEN` are for joint resolution (none silently assumed). Standalone product proposal.
**Surfaces:** repo canonical: this file; collaborative working copy: Claude Doc; team copies: Word files in Drive under Shared drives/Product/USDC Accounts (refreshed on meaningful revisions). Team copies carry no internal-workflow language.
**IDs:** decisions `W-D*`, requirements `W-R*`, open questions `W-Q*`; Privy confirmations use the shared `C-PR*`/`C-Q*` IDs (canonical in the counterparty tracker).

---

## 1. Summary

Zed offers Philippine customers a dollar-denominated account holding **USDC** in a **genuinely user-owned, self-custodied Privy wallet**, embedded as a tab in the existing Zed app. Unlike the previous architecture — which stood or fell with a single on-ramp partner — this product is built **wallet-first, in modules**: the wallet core ships without any money-movement partner at all (users fund it from wherever they already can), and merchant payments, yield, and a native on-ramp bolt on later, each as a product that can stand alone.

**Why the pivot:** the previous architecture routed its entire deposit leg through Coins.ph's inbound InstaPay/PESONet rails — exactly the capability the Bangko Sentral ng Pilipinas (BSP) suspended on 2026-09-29, with reinstatement timing unknown and the alleged abuse pattern (third parties settling with offshore-gaming operators in stablecoins) uncomfortably close in shape to a merchant pass-through on-ramp. The lesson is structural, not tactical: **no single counterparty should be able to take the whole product down.** The wallet core requires no licensed money-movement partner; every module that does require one is isolated, swappable, and optional.

### 1.1 The module map

```mermaid
flowchart TD
  M2["M2 — Merchant payments<br/>(QR Ph spend off the balance)"]
  M3["M3 — Yield<br/>(TMMF-first via Privy; DeFi vaults as alternative)"]
  M4["M4 — Native on-ramp<br/>(PDAX as candidate VASP partner)"]
  M1["M1 — Wallet core (foundation)<br/>embedded self-custodied Privy wallet:<br/>receive · hold · send USDC"]
  M2 --> M1
  M3 --> M1
  M4 --> M1
  classDef core fill:#eef3fa,stroke:#4a6fa5
  class M1 core
```

| Module | One-line product | Stands alone as | Needs a licensed money-movement partner? |
|---|---|---|---|
| **M1 — Wallet core** | An embedded, self-custodied USDC wallet: your own address to receive, hold, send | A dollar store-of-value for anyone who can already acquire USDC | **No** — pure wallet software; funding is bring-your-own on-ramp |
| **M2 — Merchant payments** | Pay any QR Ph merchant from the USDC balance | "Spend dollars anywhere QR Ph works" | Yes — **Netbank** settles the PHP leg via its QR-PH disbursement API (decided 11/17); the conversion leg is Zed PH purchase financing settled in USDC (decided 11/27, W-D13), liquidated through a VASP on Zed PH's own account (counterparty open, W-Q10) |
| **M3 — Yield** | Opt-in yield on held USDC — tokenized money market funds (TMMFs) first, decentralized-finance (DeFi) lending vaults as the alternative | A dollar savings product | No money-movement partner; instrument/venue gates instead (SRC §8 for TMMFs — design-blocking) |
| **M4 — Native on-ramp** | PHP in → USDC lands in the user's wallet | The convenience layer that completes the loop | Yes — a VASP partner; **PDAX** (Philippine Digital Asset Exchange) is the candidate; a complete partner-integration + ledger design template exists (document map, §5) |

**Build order:** M1 first — it is the only hard prerequisite; everything else bolts onto it. M2, M3, M4 are mutually independent and sequence by opportunity (current lean: M2, then M3 with TMMF-first, then M4). Priority and pilot scope per module → W-D8.

**Positioning:** "preserve wealth" over "grow savings" (peso-depreciation framing); never present yield in isolation; design for the stablecoin-literacy gap. The M1-only product targets users who can already self-fund — crypto-aware early adopters among the existing cardholder base — and that cohort choice is a feature: it validates custody UX and demand before any partner dependency exists.

## 2. Decisions

### 2.1 Settled

| # | Decision | Choice | Basis |
|---|---|---|---|
| W-D1 | Strategy | **Wallet-first, modular** (Steve, 11/12): M1 ships with bring-your-own funding; M2/M3/M4 are isolated bolt-ons, each viable alone | BSP suspension of Coins.ph inbound rails demonstrated the single-partner failure mode |
| W-D2 | Custody | User-owned, self-custodied Privy wallet; no Zed signer or keys; open-loop; all outbound user-signed | No-unilateral-Zed-signing posture; Privy configuration confirmations C-PR-1..5 apply |
| W-D3 | Stablecoin | USDC | Privy Earn USDC vaults are live self-serve; Circle issuer posture |
| W-D4 | Surface | **Standalone app (decided 11/17)** — shipped as a mobile progressive web app (PWA) for the pilot; native packaging later if warranted | 11/17 meeting — reverses the earlier in-app-tab lean: the product targets a cohort up to 10× the cardholder base and stands on its own brand; a PWA keeps iteration outside app-store review |
| W-D5 | M3 instrument order | **TMMF first**, DeFi lending vaults (Aave-family via Privy) as the alternative | Steve, 11/12; easier regulator story, countercyclical, Treasury-backed; subject to the SRC §8 gate |
| W-D6 | M1 funding model | **Bring-your-own on-ramp**: the user funds their own address from any external source; Zed builds no deposit rail into M1 | Steve, 11/12 — the de-risking core of the strategy |
| W-D7 | M2 PHP settlement partner | **Netbank (decided 11/17)**: QR Ph decode + disbursement from a prefunded Zed corporate account, via its QR-PH API (`research/netbank-qrph.md`) | 11/17 meeting; Zed has an existing Netbank relationship (items C-NB-1..7 in the Counterparty & Counsel Tracker). Covers the payout leg only — the conversion leg is W-D13 |
| W-D13 | M2 conversion structure | **Purchase financing settled by dación en pago (decided 11/27).** Zed Financial PH, Inc. ("Zed PH") — the group's licensed financing company and BSP-registered non-bank credit card issuer (NBCCI) — finances each purchase as a drawdown under a master purchase-financing agreement; the user settles the draw by conveying USDC at the quoted rate (dación en pago — payment in kind under the Civil Code), making the USDC Zed PH's property on receipt; Zed PH liquidates its own USDC through a licensed VASP on its own account (counterparty W-Q10, cadence W-Q11). Chosen over routing the user's USDC to a VASP as conversion principal (the prior lean — the liquidation VASP can still quote the till rate) and over user-owned Netbank accounts, which is preserved whole as the fallback (**Appendix A**) | Keeps conversion on Zed PH's existing licenses with no per-user bank onboarding; the financing is real, not a label — papering in W-R22, at-the-till flow in W-R23, invariants in W-R24/25; counsel pressure-test W-Q12 |

### 2.2 OPEN

| # | Decision | The question | Preliminary note |
|---|---|---|---|
| W-D8 | Module sequencing + pilot scope per module | Current lean M2 → M3 → M4; cohort + caps per module undecided | Prior working reference for M1: ~50 invite-only existing cardholders, conservative caps |
| W-D9 | Naming / brand | Current working name: **"Zed Cash"** (11/16); final naming open. Active debate (11/25): "Dollar" disfavored — limiting if other currency-backed coins follow; candidates Wallet / Cash / Stash; marketing lean "Zed Wallet"; nothing final | Steve's call + a compliance floor on USDC/Circle disclosure prominence |
| W-D10 | Chain | Lean: Base (Privy Earn USDC vaults live there) — but now gated on M3 instrument availability and M2/M4 partner rails | Chain follows the instruments and the partner rails |
| W-D11 | M1 receive guardrails | How open is "open-loop receive": any sender vs. screening/limits; multi-chain receive vs. single-chain with guidance | Interacts with W-Q3 (counsel) |
| W-D12 | KYC fields beyond the floor | Collect **source of funds**? **TIN**? Both raised 11/25 — source of funds argued internally as the one field regulators care most about (money-laundering lens); TIN as a strong is-a-real-person signal | The W-R20 floor ships regardless; adding a field later is cheap, walking one back is not |

## 3. Module requirements

Each module: the flow to build first, then requirements as capability statements with implementation detail nested beneath.

### M1 — Wallet core (the foundation)

**The flow to build:** a user comes off the waitlist and creates an account in the standalone app (W-D4, W-R19); their self-custodied Privy wallet is created (user-sole-owner, keyed to the app's own auth service via JSON Web Token bring-your-own-auth); they see their **receive address** with clear chain guidance and can share/copy it; funds they send from an exchange or another wallet appear as their USDC balance; they can **send** USDC to any address by signing the transaction themselves; everything keeps working regardless of their card-account state.

- **W-R1. Wallet creation.** User-sole-owner Privy wallet; no Zed key material; export/recovery usable independently of Zed (C-PR-3); creation idempotent and invisible-fast inside the app.
- **W-R2. Receive.** The address is first-class UX: copy/share/QR render, explicit chain labeling ("send only USDC on {chain}"), deposit detection with confirmation states, and a designed answer for wrong-asset/wrong-chain sends (recovery guidance, not silence). Chain scope per W-D10/W-D11.
- **W-R3. Send.** User-signed, open-loop to any address; fee (gas) handling defined (sponsored vs. user-paid → gas strategy from the Privy tech digest; the internal MVP sponsors gas as of 11/25 — the lasting strategy is still the open choice); address-book and safety affordances (test-send nudge, allowlist option).
- **W-R4. Balance truth.** The chain is the source of truth; no Zed ledger of user balances. Display = on-chain balance + pending in/outbound states.
- **W-R5. Card-account-state independence.** Delinquency locks the card tab, never the wallet; closed card accounts retain wallet access (empty/marketing-state pattern); forced-offboarding path designed without a partner to force it through.
- **W-R6. Compliance posture** (→ W-Q3): Zed provides self-custody wallet software; it is not custodian, exchange, or transmitter. Product must preserve that: no pooling, no Zed-controlled flow of user funds, terminology discipline. Sanctions/screening posture on receive and send per counsel.
- **W-R7. Runbooks.** Privy outage, chain congestion, compromised-device support flow, pilot halt (which, with no partner, is just feature-flagging the tab).
- **W-R19. Waitlist + account creation (standalone app).** The waitlist exists to measure demand, so friction stays minimal (decided 11/25): the marketing site drives to an **email-only** capture with a share incentive — no account creation, no app install, no access codes at signup. Invites go out by email; the invited user then creates an account (email + password, email verification, terms acceptance) and lands in the wallet with two entry actions: **Add funds** (the W-R2 receive flow) and **Unlock pay** (the W-R20 identity flow). Password rules are stricter than the card app's — the balance is uninsured and instantly movable. Onboarding forms are redesigned from scratch: the card app's components can't be reused (different stack) and its form UX is explicitly not the bar (Robinhood-grade speed is). Address entry drops the field-per-component pattern: reuse the existing region/city/barangay backend corpus and evaluate Google Address Autocomplete for Philippine coverage.
- **W-R20. Identity verification (voluntary KYC — gates pay, never the wallet).** No regulation mandates KYC for the self-custody wallet itself (§4.0); Zed collects identity proactively so the product has an identity story to show regulators and a handle for fraud management. It gates "pay"-type features only — receive, hold, and send never require it. The floor (set 11/25): **full legal name, residential address, phone number**, plus **government ID capture and a selfie match**; the ID is OCR'd to pre-fill the detail fields. Fields beyond the floor (source of funds, TIN) → W-D12. Benchmark in progress: what Coins.ph collects from Zed for travel-rule compliance, as the closest proxy for regulator expectations (feeds the W-Q3 fact package).
- **W-R21. Signing authority must be user-held — login can never move money.** Because the app's own auth service issues the JSON Web Tokens that Privy trusts (bring-your-own-auth), Zed could technically mint a valid token for any account. App login must therefore never be sufficient to sign a transaction — otherwise Zed is custodial in substance regardless of configuration (settled 11/25). Transaction signing requires a factor only the user holds — passkey, or multi-factor where passkeys are unavailable — enforced at the wallet layer; a device that can't support one can't open an account. This is the concrete mitigation for the known bring-your-own-auth residual (C-PR-2) and is what keeps W-D2's no-unilateral-Zed-signing posture true in fact, not just in settings.

### M2 — Merchant payments (QR Ph, settled via Netbank)

The user pays from a dollar balance; the merchant receives ordinary pesos over the QR Ph rails they already accept, and never needs to know crypto was involved. Making that work means every payment has two legs: a **conversion leg** (the user's USDC becomes pesos) and a **settlement leg** (pesos reach the merchant's bank). Netbank owns the settlement leg (W-D7). The conversion leg is decided (W-D13): **Zed PH finances the purchase and the user settles the financing in USDC** — the papering is W-R22, the at-the-till flow W-R23, and the invariants that keep the structure true are W-R24/25.

**The flow to build:** the user scans any QR Ph code (the Philippines' national QR payment standard); the app decodes it through Netbank (`GET /v1/qrph/decode` — merchant name and city, PHP amount for dynamic codes, person-to-merchant vs person-to-person type, and a `disburse_id`); the app shows the merchant, the PHP amount, and the USDC settlement quote (rate and any finance charge disclosed at the moment of confirmation); the user taps **Confirm payment** — a drawdown under their purchase-financing agreement, booking Zed PH's receivable — then authorizes with their user-held signing factor (W-R21), conveying USDC to Zed PH in settlement; on broadcast, the PHP leg settles via Netbank's QR-PH disbursement (`POST /v1/qrph/transactions`), which debits Zed PH's prefunded corporate account and pays the beneficiary, tracked Pending → ForSettlement → Settled. The precise ordering is load-bearing — W-R23. API detail: `research/netbank-qrph.md`.

```mermaid
flowchart LR
  subgraph UL ["At the till"]
    direction TB
    M["Merchant's QR Ph code<br/>(any participating bank<br/>or e-wallet)"] -->|"1. User scans — the app decodes<br/>via Netbank: merchant name,<br/>amount, disburse_id"| U["User's Zed Cash wallet<br/>(USDC, self-custodied)"]
    U -->|"2. Confirm payment = a drawdown under the<br/>user's purchase-financing agreement:<br/>Zed PH books a receivable (W-R22/23)"| CV["3. User signs: USDC conveyed to Zed PH<br/>in settlement (dación en pago) —<br/>Zed PH's property on receipt"]
  end
  subgraph PL ["Peso settlement — Netbank"]
    direction TB
    F["Zed PH corporate account at Netbank<br/>('the float' — Zed PH's own pesos,<br/>funded in advance)"] -->|"4. On broadcast: QR-PH disbursement pays<br/>the merchant, discharging Zed PH's OWN<br/>obligation (Pending → ForSettlement → Settled)"| MB["Merchant's bank or<br/>e-wallet account"]
  end
  UL -.->|"5. Zed PH liquidates its own USDC through<br/>a VASP (W-Q10) and replenishes the float<br/>(per-payment vs. daily batch — W-Q11)"| PL
  classDef user fill:#f2efe9,stroke:#a08c5b
  classDef bank fill:#eef3fa,stroke:#4a6fa5
  class U user
  class F,MB,CV bank
```

- **W-R8. Two legs, separately owned.**
  - The **settlement leg is Netbank's** (W-D7): Zed PH keeps a pool of its own pesos at Netbank, funded in advance (the "float"), and each merchant payment is disbursed from it — discharging Zed PH's own obligation under the drawdown (W-R22).
  - The **conversion leg is Zed PH's own treasury (W-D13):** the USDC a user conveys in settlement is Zed PH's property on receipt; Zed PH liquidates it through a licensed VASP on its own account as a principal customer — Coins.ph or PDAX, counterparty open (W-Q10) — per transaction or in a daily batch (W-Q11: a treasury-risk choice with no regulatory weight, since in both cases Zed PH converts its own property).
  - The parked alternative — **user-owned Netbank deposit accounts: no float, no credit** — is preserved whole in **Appendix A** as the fallback if the financing structure hits a roadblock, with its revive triggers stated there.
- **W-R22. The papering: one master purchase-financing agreement, drawn down per purchase.** The legal spine of M2. Zed PH papers the financing once, the way its card already does — one continuously-live agreement, each transaction a draw under it — never a contract per purchase:
  - **Executed at "Unlock pay"** (the same step as W-R20 identity verification): the user accepts a **Master Purchase-Financing Agreement** with Zed PH. From that moment a credit relationship exists continuously, so every later purchase settles against a facility that predates it by days or weeks — there is no per-purchase contract-formation moment, and the obligation always exists before any USDC moves.
  - **What the agreement establishes:** (i) Zed PH grants a purchase-financing facility (limit mechanics → W-Q12); (ii) each accepted quote is a **drawdown** — Zed PH becomes bound to pay the quoted merchant the quoted peso amount, and the user owes Zed PH that amount immediately; (iii) the user settles each drawdown by **dación en pago**: conveying USDC at the quoted rate, the transfer constituting full settlement and passing title to Zed PH on receipt; (iv) any spread between the quoted rate and the reference rate is a **finance charge**, disclosed per transaction (W-R25); (v) a drawdown whose settlement transfer fails survives as a collectible receivable under the agreement's terms.
  - **Deliberately not revolving in behavior:** the license permits revolving balances, but a draw settles within seconds by design (W-R24), so no balance persists and no interest accrual, billing cycle, or collections machinery arises on the normal path. The facility is revolving-*capable* on paper — that is what the license exists for — and bang-bang in operation.
  - **Accounting must match the paper:** each drawdown books a receivable (however briefly it lives) and its settlement books the USDC as Zed PH property at the quoted valuation. If the books say "customer funds," the contract says nothing.
- **W-R23. The Confirm-payment step: two authorities, two calls, in a fixed order.** This is where the legal structure and the self-custody architecture meet. Two different authorities act: Zed's API can create obligations but cannot move USDC; only the user's signing factor can move USDC but cannot create obligations. The ordering between them is load-bearing — the drawdown must exist before the USDC moves, and the peso disbursement fires on broadcast, not on finality.
  - **UI requirements, on one screen before any signature prompt:** merchant name and city, the PHP amount, the USDC settlement amount, the rate, the finance charge as its own line (W-R25), the quote-expiry countdown, and the facility reference (wording to be finalized with counsel — the substance: this payment is financed by Zed PH under the user's Purchase Financing Agreement). The user must be able to see they are drawing financing and settling it — not "sending money through Zed."
  - **Confirmation is two deliberate acts, never collapsed into one gesture:** the **Confirm payment** tap (the contractual act — exercising the facility) and the **passcode/passkey signature** (the settlement act — performing it). Collapsing them would blur the one sequencing fact the structure rests on.
  - **The API-call sequence:**
    1. The app `POST`s quote acceptance to the Zed API (wallet-core): the API validates quote freshness, **creates the drawdown and books the receivable**, and returns a `drawdown_id`. Only on success does the app proceed — Zed PH is now committed to pay the merchant, and the user now owes Zed PH.
    2. The app requests the signature from the Privy wallet: the user's passcode/passkey unlocks signing (key material never leaves user control — W-R21); the signed USDC transfer to Zed PH's collections address carries the drawdown attribution (W-R24) and is broadcast.
    3. The app reports the broadcast transaction hash to the Zed API against the `drawdown_id`, and **Zed PH fires the Netbank disbursement on broadcast — not on chain finality.** The seconds between broadcast and finality are genuine settlement risk borne by Zed PH, which is precisely what a financier does — and it is what gets the merchant's confirmation to card-tap speed (W-R18).
  - **Failure handling, by stage:** Stage 1 fails → nothing happened; no signature is ever requested. Stage 2 abandoned (passcode cancelled, device dies) → the drawdown expires with its quote (short time-to-live); Zed PH has disbursed nothing and the expiry cancels its commitment under the agreement. Stage 3 broadcast succeeds but the transfer later fails on-chain (reorg, revert) → the disbursement is out and the receivable survives; the agreement's retry-then-collections terms apply — this is the risk the finance charge prices. Disbursement failure after USDC receipt → Zed PH still owes the merchant under its drawdown commitment; operations runbook retries; the user's settlement stands.
- **W-R24. The bang-bang invariant: settlement flows only, never balances.** USDC moves from the user's self-custodied wallet to Zed PH **only in settlement of a drawdown created moments earlier** — never as prefunding, a deposit, or a standing balance. Concretely: no "add funds to Zed" path exists anywhere in the product; the collections address (wallet-core's vault deposit address) holds only Zed PH's own post-settlement property; the treasury sweep behind it (the CCTP sweeper to the warm wallet) is Zed PH managing its own funds; and attribution of inbound transfers is receivable bookkeeping — *which drawdown did this settle* — never user-balance accounting. This invariant is what keeps the vault a collections account rather than custody; breach it once (one prefunded peso of user money) and the custody and e-money analyses in §4.0 reopen.
- **W-R25. Characterization discipline — the words are part of the structure.** Extends W-R6's terminology discipline to M2, binding on product copy, internal documents, schemas, and ledger language: payments are **financed by Zed PH and settled by the user in USDC** — never made "on behalf of" the user; the vault is a **collections and treasury address** — never a "custody service," "wallet service," or "user balance"; the spread, when present, is a **finance charge** and is named as such (current parameter: ~1–2% and variable — the amount is open, the characterization is settled, W-D13). Rationale, per §4.0's method: internal documents asserting the adverse characterization are the cheapest evidence against the structure.
- **W-R9. Rate + total-cost disclosure** at confirmation; no spread opacity. Static QR codes carry no amount — the user enters it before quoting. The finance-charge line of W-R23's confirmation screen is the concrete form, and doubles as the Truth in Lending (RA 3765) disclosure surface (form per counsel, W-Q12).
- **W-R10. Per-payment traceability.** Decode payload, our `reference_id`, Netbank `transaction_id` + status trail, quote, rate, USDC debit tx hash — reconcilable end to end.
- **W-R18. The payment must finish while the customer is standing at the counter.** A QR Ph payment happens in person: the merchant watches their screen for the confirmation before handing over the goods. So the whole chain — decode, quote, the user's signature, Netbank's disbursement, the merchant's confirmation — has to complete reliably in a few seconds, like a card tap; "usually fast" is a failed checkout. Two concrete consequences: Netbank's API supports an approval step designed for back-office payouts (a second employee approving each disbursement — "maker-checker"); that must be configured OFF the per-payment path, or every purchase would stall at the till (→ W-Q8). And the pilot may restrict to merchant codes (person-to-merchant) only, leaving person-to-person QR transfers out of scope.

### M3 — Yield

**The flow to build:** a separate, opt-in surface under its own terms: the user moves USDC from their wallet into the yield instrument by signing themselves, watches the position, withdraws anytime by signing again. **Instrument order: TMMF first** (W-D5), reachable through the same Privy integration; DeFi lending vaults (Aave-family) as the fallback if the TMMF gate fails.

- **W-R11. The SRC §8 gate comes before design** (critical path): a tokenized money market fund offered to Philippine retail plausibly requires securities registration under the Securities Regulation Code §8 — counsel opinion **before** the yield flow is designed. Working frame (§4.0, non-definitive): the complete customer arrangement is what gets classified — neither the partner intermediation nor self-custody resolves it on its own. If it fails: the DeFi-vault alternative proceeds under the C-Q12 characterization question instead; the onchain-lending analysis supporting the venue choice is available from the product team.
- **W-R12–15. Custody + display invariants.** User-signed instrument entry/exit, positions self-custodied where the instrument allows, no Zed pooling or omnibus position; Zed's fee share to the dedicated admin wallet under key-quorum dual control; yield shown as variable, never "interest," loss-possible and liquidity disclosures, never yield in isolation.
- **W-R16. Gates before external users:** Philippine availability of the chosen Privy instrument **in writing** (C-Q6 — asked per instrument, TMMF availability/eligibility first); instrument diligence memo on the chosen venue.

### M4 — Native on-ramp (later)

**The shape:** PHP in → USDC delivered to the user's own wallet, via a VASP partner. **PDAX is the candidate** to scope. A complete partner-integration corpus already exists as the template — the **Coins.ph Integration doc** and the **PHP Ledger Design** (document map, §5): the integration question set to re-ask, the two-step deposit user experience, the interface-not-holder custody discipline, the KYC pass-through with a review-and-edit screen, and the suspense-account ledger — all restate against PDAX's actual API surface.

- **W-R17. Partner-independence invariant:** M4 (and M2) integrations are bounded modules behind interfaces, so a partner suspension disables a module, never the product. This is the W-D1 strategy expressed as an engineering requirement.
- Scoping questions → W-Q2 (PDAX capabilities: collection/virtual accounts? direct-to-external-wallet delivery? merchant KYC pass-through? InstaPay inbound?); relationship intro first.

## 4. Status board

### 4.0 Regulatory working frame — context, not conclusions

**How this section reasons (the letter-of-law method):** Philippine financial regulation assigns activities to licenses through defined text, and supervision runs along entity lines. The analyses below therefore decompose each product flow into legs, name the established legal instrument each leg already is (a loan; payment of one's own debt; a technology service), and test whether any regulation's actual text reaches that leg — rather than reasoning from a regulation's perceived purpose. Where the text is silent, that is treated as a question to raise with the regulator proactively, not a prohibition to assume. This mirrors how the Philippine market operates in practice: functionally identical products are routinely delivered through structures in which each leg sits compliantly inside its own regulator's silo. Residual risks — recharacterization on substance, future rule changes — are stated openly in each analysis as inputs to a risk decision.

The regulatory findings below draw on the **USDC-USDT PH Regulatory Research Handoff** (published alongside this document; primary sources cited there). **Nothing in this subsection is treated as definitive** — it is not a legal opinion; it frames what counsel must answer under W-Q3/W-Q4. The load-bearing points:

- **Three separate analyses, never one:** the token itself; the complete customer-facing arrangement; and each provider's regulated activities. A non-security conclusion on plain USDC decides nothing about a yield feature built on it.
- **M1's posture is the strongest case:** plain holding and transfer with no promised return carries the strongest non-security argument (the instrument "is not a security in the first place," per the investment-contract test in *Power Homes v. SEC*) — but it still requires an operating-model review (which entity performs exchange, transfer, or safekeeping under BSP Circular 1108), and no published SEC determination blanket-resolves USDC or USDT as non-securities.
- **Yield changes the question — and neither partnering nor self-custody changes the answer:** committing tokens to a return-generating arrangement may create a separate regulated instrument; "moving the promise to a third-party partner" does not resolve classification, and the research handoff's scenario matrix flags exactly M3's shape ("self-custody wallet with integrated access to an offshore yield service") as leaving promotion, intermediation, and investment-rights questions open.
- **Bring-your-own funding (W-D6) has its own wrinkle:** BSP M-2026-003 states PH-resident retail may not directly access unregistered offshore VASPs (it is addressed to BSP-supervised institutions — the research handoff cautions against reading it as making token ownership unlawful). If Zed's UX steers users toward specific external on-ramps, that Zed-linked arrangement needs explicit review → folded into W-Q3.
- **Per-token diligence is its own obligation:** BSP M-2026-023 (June 2026) requires token- and network-level listing diligence (reserves, redemption, liquidity, legal rights) with ongoing monitoring and delisting triggers — the diligence pattern partners and counsel will expect even where Zed itself is not a VASP (feeds W-D3/W-D10).
- **Standing regardless of classification:** the VASP-license moratorium continues (BSP M-2025-031 — constrains any own-license path and frames partner scarcity for M4); the Financial Products and Services Consumer Protection Act (RA 11765) disclosure duties align with the W-R12–15 display rules (never imply an insured deposit; distinguish token value from investment return; substantiate any guarantee claim).
- **Why local VASPs don't offer DeFi pooling (corroboration only — uncited analysis):** the **BSP-VASP DeFi Pooling Note** (published alongside this document) argues BSP Circular 1108's custody/safekeeping mandate, outsourcing-control rules, and the ₱50,000 FATF travel-rule threshold make VASP-pooled DeFi exposure unworkable, pushing yield products toward the SEC's perimeter. Consistent with M3's design (the user enters any instrument themselves, self-custodied and user-signed — no VASP or Zed pooling) and with treating classification as W-Q4's question — but it carries no citations, so it corroborates the frame rather than establishing it.

The handoff closes with a diligence checklist — customer entitlement, asset control, return source and calculation, operating roles, customer journey, funds flow — which this PRD adopts as **the fact package to assemble for counsel** under W-Q3/W-Q4.

**Working position — the layered defensibility argument** *(set 11/12; for counsel to pressure-test under W-Q3/W-Q4, not a settled conclusion)*:

1. **M1 is inoculated twice, by two different features.** Self-custody defeats the activity-based regimes (no exchange, transfer, or custody of others' assets — Zed ships software) and prevents any Zed-layer instrument from arising (a self-custodied token creates no claim on Zed that could be recharacterized as debt, a participation interest, or e-money). Bring-your-own funding defeats the offering question (Zed never offers, sells, or delivers USDC — users acquire it elsewhere). Residuals for W-Q3: whether constructing transactions for the user's signature could be read as "transfer on behalf of another"; the characterization of Privy's key-share infrastructure; and whether in-app promotion of holding USDC is MC 4 §7 marketing even absent any sale.
2. **Each later module deliberately re-accepts one named exposure.** M4 reintroduces offer/sale of the token (the partner sells; Zed markets the flow). M3 creates a new customer arrangement to classify. The modular build order is also a legal sequencing: the clean core ships first.
3. **M3's structure takes the worst theories off the table.** No custody, no pooling, no discretion, no Zed-issued receipt or claim; entry and exit are user-signed from the user's own wallet. That defeats "Zed operates an investment pool" and "Zed issued its own yield instrument" — the fatal outcomes. For raw protocol supply (Aave-style) there is additionally an argument that no security exists at all; note the asymmetry: a curated vault's curator reintroduces "efforts of others," and a tokenized money market fund share is a security on its own terms — so the no-security escape is instrument-dependent, and unavailable for the first-choice instrument (which is why SRC §8 sits design-blocking in front of it).
4. **What user-signed execution does not defeat: solicitation.** "Offer, sell, distribute, market" turns on who presented the opportunity, induced the decision, and was compensated — not on who signed the transaction. An integrated yield tab presenting one pre-selected instrument with a fee share to Zed is the strongest product and the thinnest form of the self-directed argument. The integration spectrum, strongest legal posture first: (a) the user exports their wallet and reaches a protocol's own frontend — outside Zed's perimeter entirely (the true content of "self-custody inoculates"); (b) education only, no in-app entry point; (c) links or a directory, no compensation; (d) the current design — integrated single-instrument flow with a fee share. **The two dials counsel must price: curation/presentation, and compensation.**
5. **PH VASPs' absence from DeFi access corroborates the structure, not the risk.** A custodial platform's version is worst-case by construction: supplying a pool breaches the Circular 1108 safekeeping mandate, constitutes investment management outside the money-service-business perimeter, converts the customer's claim into the VASP's own unregistered arrangement, and fails the outsourcing-recourse and travel-rule-beneficiary requirements. The clean version of the trade exists only in a non-custodial architecture — structural precedent: Robinhood Earn's self-custodial Morpho supply. Cautions: the licensed incumbents' unanimous abstention also reads as regulator temperature, untested waters are not safe waters, and the promotion half of their problem remains ours in miniature.
6. **The question for counsel is therefore not "does self-custody make this permissible."** It is: given no custody, no pooling, no discretion, and no Zed instrument, what combination of curation, presentation, and compensation keeps the integrated flow on the right side of offer, solicitation, and marketing — and what product features would we trade to stay there?

**Applied analysis — Operator of Payment Systems (OPS) and M2** *(working analysis using the method above; not a legal opinion)*

The question: does M2 require Zed to register as an Operator of Payment Systems under the National Payment Systems Act (RA 11127) and BSP Circular 1049? The governing text: the statute's §4 defines an operator as one who "provides clearing or settlement services in a payment system, or defines, prescribes, designs, controls or maintains the operational framework for a payment system"; Circular 1049 adds one who "maintains the platform that enables payments or fund transfers," "operates the system or network," or "provides a system that processes payments on behalf of any person." **Working answer: no — no M2 leg performed by Zed falls within the text**, and the BSP's August 2025 determination that **Apple Pay and Google Pay are not OPS** is directly on point (no fund-holding; credentials/instructions only; "money does not pass through" their systems; per Deputy Governor Tangonan, "their activity is not an OPS activity," and the accountable party is the supervised payment service provider that uses them).

| Leg | Performed by | Instrument | Nearest OPS text | Does it reach Zed? |
|---|---|---|---|---|
| QR decode | Netbank (its API) | Bank information service | "maintains the platform…" | It is Netbank's platform; Zed passes a string; no funds involved |
| Payment initiation | Zed, on its own corporate account | A bank customer instructing its own bank | — | No — the NPSA regulates systems and their operators, not payers; end-users are not operators |
| Clearing + settlement | Netbank / InstaPay (PPMI) | BSFI participation in a designated payment system | "provides clearing or settlement services" | Reaches Netbank and the clearing house — both already inside the framework; never Zed |
| The disbursement's purpose | Zed discharging its own payment obligation | Payment of one's own debt (financing wrapper) | "processes payments on behalf of any person" | No — Zed is the payer, not a processor. **This clause is the live wire; the financing characterization is what defeats it** |
| The app layer | Zed's software calling Netbank's API | Technology provision | "maintains a platform that enables payments" | The Apple Pay/Google Pay precedent: no fund-holding, instructions only, pesos move Netbank → merchant bank without touching Zed's systems |

Three design consequences worth building to:

1. **User funds never enter the peso payment system at all** — they are self-custodied USDC on-chain. The only payment-system flows in M2 are Zed's own account to the merchant's bank, through a supervised institution.
2. **In the decided structure (W-D13), the financing characterization is what the OPS position rests on** — "Zed pays merchants for users" invites the clause; "Zed PH discharges its own obligation, created by financing the purchase" does not. W-R22–25 exist to keep that characterization true in paper, code, and words. The design that needs no financing at all — removing Zed from the funds path entirely via user-owned accounts — is preserved as the fallback in Appendix A.
3. **The accountability model matches the Apple Pay determination:** BSP supervises Netbank; Netbank assesses and oversees its technology counterparties under its own outsourcing framework; Zed answers to Netbank, not to a registration of its own.

**How the decided structure stands clear of the clause, illustrated.** The one Circular 1049 clause that could reach Zed — "processes payments on behalf of any person" — is defeated by the financing characterization (W-D13): Zed PH finances the purchase, so the float disbursement discharges Zed PH's own obligation to the merchant; the user owes Zed PH, and settles by conveying USDC (dación en pago). Zed PH is a payer, never a processor. For this to hold, the financing must be real — documented terms (the W-R22 master agreement), a booked receivable, collection rights — not a label:

```mermaid
flowchart LR
  subgraph CL ["Crypto leg — Zed PH's own treasury"]
    direction TB
    U["User's wallet<br/>(USDC, self-custodied)"] -->|"2. User settles the drawdown:<br/>USDC conveyed to Zed PH<br/>(dación en pago — Zed PH's<br/>property on receipt)"| V["Zed PH liquidates its own USDC<br/>through a licensed VASP,<br/>as a principal customer (W-Q10/11)"]
  end
  subgraph PL ["Peso leg — Zed PH pays its OWN debt"]
    direction TB
    Z["Zed PH's corporate account<br/>at Netbank (Zed PH's pesos — 'the float')"] -->|"1. Zed PH pays the merchant,<br/>discharging its OWN obligation:<br/>the drawdown financed the purchase and<br/>booked a receivable against the user"| MB["Merchant's bank or<br/>e-wallet account"]
  end
  CL -->|"3. Liquidation proceeds<br/>replenish the float"| PL
  classDef user fill:#f2efe9,stroke:#a08c5b
  classDef bank fill:#eef3fa,stroke:#4a6fa5
  class U user
  class Z,MB,V bank
```

The second way to stand clear of the clause — no Zed payment existing at all, because each user pays from their own Netbank deposit account — needs no financing characterization and is preserved as the parked fallback, with its analysis and funds-flow diagram, in **Appendix A**.

Residuals, named plainly: Circular 1049 carries a Monetary Board catch-all, and a BSP **exposure draft on merchant payment acceptance activities** is pending — either could redraw this perimeter prospectively (monitor; raise in the Netbank scoping, W-Q8). At consumer scale the BSP can take interest regardless of text. The fallback is unusually cheap: OPS is a *registration*, not a licence, with no moratorium — if the BSP ever insists, registering is a modest concession, at the cost of a direct BSP supervision touchpoint on the Zed Cash entity. → W-Q9.

### 4.1 Open questions

| ID | Question | Blocks | Status |
|---|---|---|---|
| W-Q1 | M2 settlement partner for the PHP payout leg | M2 | **Closed 11/17: Netbank** (QR-PH decode + disbursement; prior relationship). The conversion leg continues as W-Q7 |
| W-Q7 | M2 conversion leg: choose the structure | M2 build | **Closed 11/27: the financing structure (W-D13)** — master purchase-financing agreement, per-purchase drawdown, dación en pago settlement, own-account VASP liquidation. Papering W-R22, flow W-R23, invariants W-R24/25; user-owned accounts parked as the fallback (Appendix A). Successor questions: W-Q10 (liquidation VASP), W-Q11 (cadence), W-Q12 (counsel) |
| W-Q10 | Liquidation VASP for the conversion leg: **Coins.ph vs PDAX** — rate quality, API latency if conversion is per-payment, settlement timing into the Netbank float, relationship health (W-Q6 weighs against Coins.ph; W-Q2 covers the PDAX intro) | M2 treasury | Open |
| W-Q11 | Conversion cadence: **per-transaction** (rate locked at pay time, hedged 1:1, the VASP's API joins the latency-sensitive path) vs **daily batch** (spread flexibility; Zed PH carries intraday USDC/PHP price risk on its own book). A treasury-risk decision with no regulatory weight — in both cases Zed PH converts its own property as a principal customer | M2 treasury ops | Open |
| W-Q12 | Counsel: pressure-test the financing structure (W-D13/W-R22-23). (i) Master-agreement drafting so each drawdown's obligation is perfected at quote acceptance, with dación settlement enforceable as drafted; (ii) underwriting formality expected for granting the facility at Unlock pay, given the credit risk is seconds of settlement risk; (iii) facility-limit mechanics (nominal standing limit vs per-transaction); (iv) whether this non-card financing product sits under Zed PH's NBCCI perimeter or its plain financing-company authority — which disclosure/pricing rulebook applies; (v) finance-charge treatment: Truth in Lending (RA 3765) disclosure form, and whether any BSP pricing ceiling reaches the spread. Reference: the M2 financing policy memo (includes an illustrative master agreement) | M2 launch | Open — the structured successor to W-Q7's counsel ask |
| W-Q8 | Netbank QR-PH integration scoping: auth scheme, webhook coverage vs polling, settlement timing per rail, fees/limits, P2M coverage, corporate-account setup, maker-checker configuration off the per-transaction path, sandbox; Account-as-a-Service items (now for the Appendix A fallback only): consumer accounts as a QR-PH disbursement source, the user-consent/mandate model for API-initiated payments from consumer accounts, per-account economics and KYC flow | M2 | Open — route via the existing Netbank relationship (contacts in the Counterparty & Counsel Tracker) |
| W-Q9 | OPS: does M2 require Zed to register as an Operator of Payment Systems (RA 11127 / Circular 1049)? | M2 launch | Working answer in §4.0: **no** — under the decided structure (W-D13) the financing characterization makes Zed PH a payer of its own debt (and the Appendix A fallback would remove Zed from the funds path entirely); Apple Pay/Google Pay precedent; counsel to confirm with W-Q12; monitor the merchant-payment-acceptance exposure draft; registration held as the cheap fallback |
| W-Q2 | PDAX capability + appetite scan — re-ask the integration question set from the Coins.ph Integration doc (document map, §5) | M4 | Open — needs relationship intro |
| W-Q3 | Counsel: characterization of M1 — self-custody wallet software provided by a PH-facing app: any VASP/EMI/money-transmission trigger? Screening obligations on open-loop receive/send? Travel-rule exposure on sends? Plus (§4.0): does UX that steers users to specific external on-ramps create a reviewable Zed-linked arrangement under BSP M-2026-003? Fact package = the §4.0 diligence checklist | M1 external launch | Open |
| W-Q4 | Counsel: TMMF / SRC §8 (C-Q14). Frame per §4.0: the complete arrangement is what gets classified — neither Privy’s intermediation nor self-custody resolves it | M3 design start | Open — **critical path now** |
| W-Q5 | Privy: TMMF instrument availability + PH eligibility in writing (C-Q6 pattern, per instrument) | M3 | Open |
| W-Q6 | Coins.ph relationship: suspension status, reinstatement timeline, their account of the cause — keeps M4 optionality honest | M4 optionality | Open — relationship-level, not API-level. Engineering signal (11/18): Coins' support for third parties like Zed is narrowing — treat the option as weakening |

### 4.2 Partner items (canonical in the shared counterparty tracker)

C-PR-1..5 (user-sole-owner config, no Zed signer, export/recovery, open-loop sends) — gate **M1**; sandbox verification is the next concrete engineering step. Privy Earn/TMMF items gate M3.

### 4.3 Next steps

1. M1 build: internal MVP is live as a progressive web app (account creation, receive, send, wallet history; gas sponsored as of 11/25). Next: waitlist + onboarding per W-R19, identity flow per W-R20, the W-R21 user-held signing factor; formal verification of C-PR-1..5 under Zed's config.
2. Counsel asks, in parallel: W-Q3 (M1 characterization — needed before external users) and W-Q4 (SRC §8 — needed before M3 design).
3. Privy: TMMF availability + PH eligibility in writing (W-Q5).
4. Netbank: kick off QR-PH integration scoping (W-Q8) through the existing relationship. The conversion structure is decided (W-D13): route the M2 financing policy memo and the W-Q12 questions to counsel **before the send-to-settlement build** (the code currently stops at the quote screen — the next engineering step is the one the papering must precede); choose the liquidation VASP (W-Q10) and the conversion cadence (W-Q11).
5. PDAX introduction (W-Q2); hold W-Q6 (Coins.ph status) warm.
6. Pilot definition for M1-only (W-D8): cohort, caps, success metrics for a bring-your-own-funding wallet.

## 5. Document map

All referenced documents are published alongside this PRD in the same folder; engineering sources live in the project repo.

| Document (this folder) | What it holds |
|---|---|
| Netbank QR-PH — API Digest | M2 settlement-leg API detail: decode and disbursement endpoints, transaction statuses, open integration items |
| USDC-USDT PH Regulatory Research Handoff | The primary-source regulatory research behind §4.0: securities classification, yield scenarios, the BSP/SEC instrument map |
| BSP-VASP DeFi Pooling Note | Context on why local VASPs do not pool customer funds into DeFi protocols (uncited research; corroboration only) |
| Coins.ph Integration — Technical Doc | The prior on-ramp partner integration; the question template for any VASP partner (M4) |
| PHP Ledger Design (Unconverted Balances) | The M4 ledger template: suspense-account mirror, cash-in / conversion / cash-out postings |
| Privy Earn — How It Works · Privy Platform — Technical Digest | M1/M3 mechanics: custody statements, wallet actions, Earn, gas, governance quorums |
| Counterparty & Counsel Tracker | Partner and counsel confirmations — the C-PR / C-NB / C-Q items referenced throughout this PRD |

## Appendix A — Parked fallback: user-owned Netbank accounts (Account-as-a-Service)

**Status: parked 11/27, not rejected.** This was the third candidate structure for M2's conversion leg while that question was open. The financing structure won (W-D13) because it keeps conversion on Zed PH's existing licenses with no per-user bank onboarding — but this alternative is preserved whole because it is the strongest possible fallback: it needs no financing characterization at all. **Revive triggers:** counsel declines to bless the perfection-at-acceptance papering or the dación settlement mechanics (W-Q12); the BSP's pending merchant-payment-acceptance exposure draft lands adversely on the financing design; or the drawdown/receivable machinery proves unenforceable or operationally brittle at scale.

**The structure: no float, no credit.** Each user holds a deposit account at Netbank in their own name, opened through Netbank's Account-as-a-Service capability (bank KYC at onboarding). Conversion proceeds from the user's USDC settle into the user's own account, and the QR payment is the user instructing their own bank, with the Zed app as the interface. Zed touches no funds at any step — the cleanest shape across the Operator of Payment Systems, e-money, and custody questions. Its costs: per-user bank KYC friction and Netbank's appetite at scale; and either the conversion partner enters the at-the-counter critical path (per-payment conversion) or the product becomes two-step — the user pre-converts and spends from a peso balance in their own account. Capability and consent-mandate questions are parked inside W-Q8's Account-as-a-Service items.

**Why it stands clear of the OPS clause without financing: there is no Zed payment at all.** Zed holds no funds and no float; the operator is Netbank; the app only passes the user's instructions — the same fact pattern under which the BSP found Apple Pay and Google Pay not to be Operators of Payment Systems. No financing characterization is needed; the option's costs are product trade-offs, not regulatory ones:

```mermaid
flowchart LR
  subgraph CL ["Crypto leg"]
    direction TB
    U["User's wallet<br/>(USDC, self-custodied)"] -->|"1. User signs USDC<br/>over to the VASP"| V["Licensed VASP"]
  end
  subgraph PL ["Peso leg — entirely the user's own account"]
    direction TB
    UA["User's OWN deposit account<br/>at Netbank (Account-as-a-Service;<br/>bank-KYC'd)"] -->|"3. User instructs payment from<br/>their own account; the Zed app is the<br/>interface, Netbank executes over QR Ph"| MB["Merchant's bank or<br/>e-wallet account"]
  end
  CL -->|"2. Peso proceeds settle into<br/>the user's own account"| PL
  classDef user fill:#f2efe9,stroke:#a08c5b
  classDef bank fill:#eef3fa,stroke:#4a6fa5
  class U,UA user
  class V,MB bank
```

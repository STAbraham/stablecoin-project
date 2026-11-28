# M2 Purchase Financing — Policy Proposal for Counsel & Compliance Review

**Status:** Draft v0.1 (2026-11-27). A proposal for review, not a legal opinion. Prepared for external counsel and internal compliance; product canon lives in the Zed Dollar Wallet — Modular PRD (W-D13, W-R22–25).
**Entity:** Zed Financial PH, Inc. ("Zed PH") — SEC-registered financing company (RA 8556) and BSP-registered non-bank credit card issuer (NBCCI, RA 10870).
**The ask:** pressure-test the structure (§2–4) against the questions in §6, and mark up the illustrative agreement in Annex A.

---

## 1. What the product does

Zed Cash (working name) gives Philippine retail customers a self-custodied USDC wallet — the user alone holds the keys; no Zed entity can move their funds. Module M2 lets that user pay any QR Ph merchant: the user spends from a dollar balance, the merchant receives ordinary pesos over the QR Ph rails they already accept, in seconds, and never knows crypto was involved.

Every payment therefore has two legs: pesos must reach the merchant (settled by Netbank, disbursed from Zed PH's prefunded corporate account), and the user's USDC must become pesos. **This memo is about the second leg** — specifically, the legal structure under which the user's USDC passes to Zed PH and Zed PH's pesos pass to the merchant.

## 2. The structure, leg by leg

The design principle (consistent with the group's regulatory posture): decompose the flow into legs, make each leg an established legal instrument, and let each leg sit inside the license that already covers it.

| # | Leg | Instrument | Performed by | License / basis |
|---|---|---|---|---|
| 1 | Facility grant at onboarding ("Unlock pay") | Master purchase-financing agreement (continuing credit facility) | Zed PH ↔ customer | Zed PH's financing-company authority (RA 8556); NBCCI registration |
| 2 | Quote acceptance at the till ("Confirm payment") | **Drawdown** under the facility: Zed PH becomes bound to pay the merchant; the customer becomes indebted to Zed PH, due immediately | Zed PH ↔ customer | The master agreement (leg 1) |
| 3 | The customer's USDC transfer | **Dación en pago** (Civil Code art. 1245): conveyance of the agreed USDC amount at the quoted rate, constituting full settlement of the drawdown; **title passes to Zed PH on receipt** | Customer (self-signed from their own wallet) | Performance of the contract |
| 4 | Peso disbursement to the merchant | Zed PH discharging **its own obligation** created in leg 2, from its own prefunded account, via Netbank's QR-PH rails | Zed PH (through Netbank, a BSP-supervised bank) | Payment of one's own debt; Netbank holds the payment-system role |
| 5 | Liquidation of the received USDC | Own-account sale of Zed PH's own property through a licensed VASP, as an ordinary principal customer (per transaction or in daily treasury batches) | Zed PH | The VASP's license covers the exchange service; Zed PH is its customer |

Two sequencing facts carry the structure:

- **The obligation always predates the USDC.** The facility (leg 1) exists days or weeks before any purchase; each drawdown (leg 2) is perfected at quote acceptance — one deliberate tap *before* the signature that moves USDC (leg 3). The customer's transfer therefore always settles an existing debt; at no moment does Zed PH hold customer value with no obligation attached.
- **Zed PH pays the merchant on broadcast, not on chain finality.** The disbursement (leg 4) fires when the customer's transaction is broadcast, seconds before it is final. In that window Zed PH has irrevocably paid while the customer's settlement could still fail — genuine settlement risk, borne by the financier, priced by the finance charge. The financing is real in substance, not only in drafting.

## 3. The papering

One master agreement, drawn down per purchase — the model the entity's card business already uses (one continuously-live cardholder agreement; each transaction a draw). Deliberately **not** a contract per purchase: a per-purchase contract would create a fresh formation moment to attack on every transaction and would reintroduce the race between contract and transfer that the master structure eliminates.

Key terms (drafted in full in Annex A):

1. **Execution:** accepted at "Unlock pay," the step where the customer also completes identity verification. No purchase is possible before the agreement exists.
2. **Drawdowns:** each accepted quote is a drawdown — Zed PH bound to pay the named merchant the quoted peso amount; the customer indebted for that amount plus any finance charge, due immediately.
3. **Settlement by dación en pago:** the customer settles by transferring the quoted USDC amount to Zed PH's designated collections address; the parties agree the conveyance at the quoted rate constitutes full settlement, with title passing on receipt. The quoted rate is the agreed dación valuation, fixed and disclosed before the customer accepts.
4. **Finance charge:** any spread between the quoted rate and the reference rate is a finance charge, disclosed per transaction before acceptance (current product parameter: on the order of 1–2%, variable; the amount is a business setting — the characterization is fixed).
5. **Non-revolving in operation:** the license permits revolving balances, but a draw settles within seconds by design; no balance persists on the normal path, so no interest accrual or billing cycle arises. The facility is revolving-capable on paper, bang-bang in operation.
6. **Failed settlement:** a drawdown whose settlement transfer fails (abandoned signature → the drawdown expires with its quote, nothing disbursed; on-chain failure after disbursement → the receivable survives) is handled under the agreement's retry-then-collections terms — the ordinary machinery of a financing company.
7. **Accounting mirrors the paper:** each drawdown books a receivable, however briefly it lives; its settlement books the USDC as Zed PH property at the quoted valuation. No ledger line anywhere reads as customer funds held.

## 4. Regulatory positions this structure takes

*(Working analyses under the letter-of-law method; each names its residual. Fuller treatment: PRD §4.0.)*

- **Operator of Payment Systems (RA 11127 / BSP Circular 1049): not triggered.** The only clause that could reach Zed is "provides a system that processes payments **on behalf of any person**." Under this structure Zed PH is a **payer**, never a processor: the disbursement discharges Zed PH's own drawdown obligation. The BSP's August 2025 determination that Apple Pay and Google Pay are not OPS (no fund-holding; instructions only; the supervised payment service provider is the accountable party) covers the app layer. *Residual:* the characterization must be real — hence the booked receivable, the real settlement risk at broadcast, and the terminology discipline; a pending BSP exposure draft on merchant payment acceptance could redraw the perimeter prospectively. Fallback if ever required: OPS is a registration, not a license — cheap to concede.
- **VASP licensing (BSP Circular 1108): not triggered.** The circular's covered activities — exchange, transfer, safekeeping of virtual assets — attach when performed **as a service for the account of others**. The customer's wallet is self-custodied (no safekeeping by any Zed entity); the USDC Zed PH receives is its own property from the moment of dación (no custody of customer assets); the conversion is Zed PH selling its own property through a licensed VASP as that VASP's customer (no exchange service offered to anyone). *Residual:* recharacterization on substance if the invariants slip — which is why "no standing balances" is a product invariant, not a habit (§5).
- **E-money / deposit-taking: not triggered.** No customer value is ever held by Zed PH awaiting instructions: funds arrive only as settlement of a debt, and no product path exists for a customer to place a balance with Zed. Nothing is redeemable; nothing is stored.
- **Consumer credit obligations: accepted, deliberately.** The structure makes every payment an extension of credit by a licensed financing company, and the product accepts the obligations that follow: Truth in Lending Act (RA 3765) disclosure of the finance charge at or before acceptance (the confirmation screen is the disclosure surface), and RA 11765 conduct standards. This cost is also the structure's strength — a disclosed charge for a real credit service is what makes the financing characterization undeniable.

## 5. Invariants the product enforces

These are engineering requirements in the PRD (W-R23–25), restated here because the legal analysis assumes them:

1. **Order of operations:** drawdown created (Zed API) → customer signature (user-held passkey/passcode; key material never leaves the customer) → disbursement on broadcast. No signature is ever requested before the drawdown exists.
2. **Two deliberate acts at the till:** the Confirm-payment tap (contractual act) and the signature (settlement act) are separate gestures, never collapsed.
3. **Bang-bang settlement, never balances:** USDC moves to Zed PH only in settlement of a drawdown created moments earlier. No prefunding, no deposits, no "add funds to Zed" path exists. The collections address and the treasury sweep behind it handle only Zed PH's own post-settlement property; attribution of inbound transfers is receivable bookkeeping, never balance accounting.
4. **Characterization discipline in words:** payments are *financed by Zed PH and settled by the customer in USDC* — never made "on behalf of" the customer; the collections infrastructure is never described as custody, a wallet service, or user balances — in product copy, internal documents, schemas, and ledger language alike.

## 6. Questions for counsel

1. **Drafting:** does Annex A's structure achieve perfection of each drawdown's obligation at quote acceptance, with the dación settlement enforceable as drafted (valuation fixed by the quote; title passing on transfer)? What would you change?
2. **Underwriting formality:** what, if anything, do the SEC/BSP expect by way of credit evaluation when the facility is granted at Unlock pay, given that economic exposure per draw is seconds of settlement risk? Is a nominal facility limit with per-transaction caps sufficient?
3. **Perimeter:** does this non-card financing product sit under Zed PH's NBCCI registration or its plain financing-company authority — and which disclosure/pricing rulebook follows?
4. **Finance charge:** the RA 3765 disclosure form for a charge expressed as an exchange-rate spread; and whether any BSP pricing ceiling (e.g., the credit-card rate caps) could be argued to reach it.
5. **Failed-settlement path:** any consumer-protection constraints on the retry-then-collections mechanics for a defaulted drawdown (notice, cooling-off, collection conduct)?
6. **The broadcast window:** any concern with disbursing on broadcast rather than finality — i.e., with Zed PH deliberately bearing that settlement risk as part of the financing?
7. **Confirmation-screen language:** approve or redraft the facility-reference wording shown at Confirm payment.

## 7. Fallback preserved

If this structure fails review, the parked alternative needs no financing characterization at all: each customer holds their own deposit account at Netbank (Account-as-a-Service), conversion proceeds settle into the customer's own account, and the QR payment is the customer instructing their own bank, with the Zed app as interface — no Zed payment exists anywhere in the flow. Full write-up, trade-offs, and funds-flow diagram: PRD Appendix A.

---

## Annex A — Illustrative Master Purchase-Financing Agreement

> **DRAFT — FOR DISCUSSION ONLY, NOT FOR EXECUTION.** Prepared to make the structure concrete for review. Bracketed items are placeholders; counsel owns the final text.

**MASTER PURCHASE-FINANCING AGREEMENT**

This Agreement is entered into between **Zed Financial PH, Inc.**, a corporation organized under the laws of the Republic of the Philippines, with SEC Registration No. [●] and Certificate of Authority to Operate as a Financing Company No. [●] ("**Zed PH**"), and the undersigned customer (the "**Customer**"), upon the Customer's electronic acceptance within the [Zed Cash] application (the "**App**").

**Recitals.** Zed PH is a financing company and registered non-bank credit card issuer. The Customer holds digital assets in a wallet under the Customer's sole custody and control. The Customer wishes to make purchases from merchants payable in Philippine Pesos, financed by Zed PH and settled by the Customer in digital assets, on the terms below.

**1. Definitions.**
- "**Facility**" — the purchase-financing facility granted under Section 2.
- "**Quote**" — an offer presented in the App for a specific merchant payment, stating: the merchant, the Peso Amount, the Settlement Amount, the Quoted Rate, any Finance Charge, and an expiry time.
- "**Drawdown**" — the extension of financing arising upon the Customer's acceptance of a Quote (Section 3).
- "**Peso Amount**" — the Philippine Peso sum Zed PH becomes obligated to pay the merchant under a Drawdown.
- "**Settlement Asset**" — USD Coin (USDC), [issuer/network description].
- "**Settlement Amount**" — the quantity of the Settlement Asset stated in the Quote, being the Peso Amount plus any Finance Charge, converted at the Quoted Rate.
- "**Quoted Rate**" — the Peso-per-USDC rate stated in the Quote, which the parties agree is the valuation of the Settlement Asset for purposes of Section 4 for that Drawdown.
- "**Finance Charge**" — the charge for the financing under a Drawdown, disclosed in the Quote before acceptance.
- "**Collections Address**" — the blockchain address designated by Zed PH in the App for receipt of Settlement Transfers.

**2. The Facility.** Zed PH grants the Customer a continuing purchase-financing facility of up to [₱ ●] outstanding at any time (the "Facility Limit"), subject to per-transaction limits stated in the App. This Agreement is a continuing agreement: it governs every Drawdown without further execution, and each Drawdown is a separate extension of financing under it. The Facility creates no obligation on Zed PH to accept any particular Quote request and may be suspended or reduced as provided in Section 8.

**3. Drawdowns.** The Customer requests financing by accepting a Quote in the App before its expiry. **Upon acceptance:** (a) Zed PH becomes bound to pay the Peso Amount to the merchant identified in the Quote, through its own account and its banking counterparties; and (b) the Customer becomes indebted to Zed PH in the amount of the Peso Amount plus the Finance Charge, **due and payable immediately**. The parties intend and agree that the obligations in (a) and (b) arise at acceptance, prior to and independently of the Settlement Transfer.

**4. Settlement by Dación en Pago.** The Customer settles each Drawdown by transferring the Settlement Amount to the Collections Address (the "**Settlement Transfer**"). The parties agree, pursuant to Article 1245 of the Civil Code, that the Settlement Transfer constitutes **dación en pago**: the conveyance of the Settlement Asset at the Quoted Rate in full settlement of the Customer's obligation under that Drawdown. **Title to the transferred Settlement Asset passes to Zed PH upon receipt at the Collections Address**, free of any claim of the Customer, and Zed PH may deal with it as its own property in all respects. A Settlement Transfer initiated in the App contemporaneously with acceptance is acknowledged as the intended ordinary course.

**5. Finance Charge; Disclosure.** The Finance Charge for each Drawdown is disclosed in the Quote before acceptance, together with the Peso Amount, the Quoted Rate, and the Settlement Amount, in the form required by the Truth in Lending Act (RA 3765) and its regulations. No charge applies to a Quote not accepted.

**6. Quote Expiry; Cancellation.** A Quote not accepted by its expiry lapses. If, after acceptance, the Settlement Transfer is not broadcast before the Quote's expiry, the Drawdown is automatically cancelled: Zed PH's payment obligation and the Customer's indebtedness under it are extinguished, and no Finance Charge applies, provided Zed PH has not yet disbursed.

**7. Failed Settlement.** If Zed PH has disbursed the Peso Amount and the Settlement Transfer fails, is reversed, or is not received (including by blockchain reorganization or transaction failure), the Customer's indebtedness under the Drawdown subsists. The App will prompt a replacement Settlement Transfer; if none is received within [●] days, the amount is collectible as a past-due receivable under Zed PH's standard terms, including [late charge/interest at ●% per month] from the [●]th day. Zed PH's acceptance of a replacement transfer at the original Quoted Rate within [●] is [provided for / at Zed PH's option].

**8. Facility Limit; Suspension; Termination.** Zed PH may reduce the Facility Limit, suspend new Drawdowns, or terminate the Facility prospectively at any time with notice in the App, including for risk, compliance, or regulatory reasons. Termination does not affect accrued obligations. The Customer may terminate at any time; termination is effective when no Drawdown remains outstanding.

**9. Representations; Verification.** The Customer represents that they act on their own behalf; that the Settlement Asset transferred is their own property, lawfully acquired; and that the identity information provided at verification is accurate. Drawdowns are available only while the Customer's identity verification remains valid. Zed PH may decline Quotes or suspend the Facility for sanctions, fraud, or financial-crime reasons.

**10. No Deposit; No Custody.** Nothing in this Agreement constitutes a deposit, e-money issuance, or the safekeeping of the Customer's assets by Zed PH. The Customer's wallet remains under the Customer's sole custody and control at all times; Zed PH receives the Settlement Asset only as its own property upon settlement under Section 4. Zed PH provides no exchange, transfer, or custody service in respect of the Customer's digital assets.

**11. General.** [Notices in-App; electronic contracting (E-Commerce Act, RA 8792); amendment with notice, continued use as acceptance for prospective terms; assignment by Zed PH; severability; data privacy incorporation; complaints and consumer-assistance mechanism per RA 11765.]

**12. Governing Law; Venue.** This Agreement is governed by the laws of the Republic of the Philippines. Venue: [●].

*Accepted electronically by the Customer in the App on the date recorded in Zed PH's records.*

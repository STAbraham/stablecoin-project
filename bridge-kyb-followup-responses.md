# Bridge KYB follow-up — draft responses (2026-11-23)

> **NOTES FOR STEVE — do not paste this block.**
> 1. **Decision needed on Q4 (account use):** the KYB started under the OUSD architecture. Two framings are drafted — pick one. Option A (recommended) describes the use generically and accurately (stablecoin issuance/redemption + corporate treasury for a dollar wallet product) without naming a token, which stays true through the USDC pivot. Option B is the narrower treasury-only framing if you want to minimize scope of review.
> 2. **Insert before sending:** entity registration numbers (marked `[...]`), card network name, incorporation jurisdiction, and the two operating-activity artifacts.
> 3. **Artifacts to gather for Q2:** one recent cardholder billing statement (redact PII except name/date/amount) + the matching repayment credit shown on Zed's bank/collection account statement. If easier, a settlement report from the processor works as secondary evidence.
> 4. The licensure/exemption answer deliberately describes each activity by its established name and says nothing beyond what's asked — don't expand it verbally if they follow up by phone; ask them to put questions in writing.

---

## 1. Nature of business — what does the business sell or provide, and to whom?

Zed Financial, Inc. ("Zed") is a consumer credit card issuer serving residents of the Philippines. Zed issues the Zed Card, a [Visa/Mastercard] credit card, to individual retail customers who apply through our mobile app and are onboarded with full identity verification (KYC performed via Persona) and credit underwriting. We currently serve approximately 11,000 cardholders.

Our revenue comes from interest on revolving balances and installment plans, interchange, and card fees. Our customers are exclusively individual consumers in the Philippines; we do not serve businesses, and we do not serve customers outside the Philippines.

Zed is also developing a dollar-denominated account product ("Zed Cash," working name) that will let the same consumer base hold and use US-dollar stablecoins in self-custodied wallets. This is the product line for which we are onboarding with Bridge (see item 4).

## 2. Proof of operating activity

As a business-to-consumer credit card issuer, our equivalent of a "customer invoice" is the monthly cardholder billing statement. Attached:

1. **[ATTACH]** A recent monthly billing statement issued to a cardholder (customer personal details redacted beyond name and statement date), showing the amount billed; and
2. **[ATTACH]** The matching payment evidence: the corresponding repayment credit received into Zed's collection account, as shown on our bank statement / payment-rail confirmation (InstaPay/PESONet reference included).

We are happy to provide additional months, additional statement/payment pairs, or processor settlement reports if useful.

## 3. Proof of licensure / explanation of exemption

**For our current operating activity (consumer credit card issuance):**

Zed Financial, Inc. is registered with the Philippine Securities and Exchange Commission [SEC Registration No. ___] and holds a Certificate of Authority to operate as a financing company under Republic Act No. 8556 (the Financing Company Act) [Certificate No. ___]. Our credit card issuing business is conducted under Republic Act No. 10870 (the Philippine Credit Card Industry Regulation Law) [and is registered with the Bangko Sentral ng Pilipinas accordingly — Ref. No. ___]. **[ATTACH: SEC Certificate of Registration; Certificate of Authority; any BSP registration/acknowledgment.]**

**For the planned stablecoin-related activity (the subject of this Bridge account) — explanation of why no additional license is required:**

Zed's role in the planned product is confined to activities that do not require a virtual-asset license under Philippine regulation, because each regulated function in the product sits with a party licensed to perform it:

- **Custody:** customer wallets are self-custodied. Wallet key material is generated and held under the customer's sole control through our wallet infrastructure provider; Zed holds no keys, cannot transact on a customer's behalf, and never takes possession of customer assets. Zed therefore does not perform safekeeping or administration of virtual assets for others.
- **Issuance and redemption:** stablecoin issuance and redemption are performed by Bridge as the licensed issuer/money-services provider, settling directly with customers' self-custodied wallets or with Zed's own corporate account.
- **Exchange:** Zed does not offer exchange between virtual assets and fiat as a service to others. Any conversion activity on Zed's own corporate funds is own-account treasury activity executed through licensed counterparties.
- Under BSP Circular No. 1108 (Series of 2021), virtual asset service provider licensing attaches to entities providing exchange, transfer, or custody of virtual assets **as services to others**. Zed performs none of these functions; it provides the customer application and interface, while licensed counterparties perform the regulated legs. Zed's existing consumer-credit activities remain licensed as described above and are unaffected.

Zed monitors this analysis against regulatory developments and would seek the appropriate authorization before undertaking any activity that requires one.

## 4. How the entity will use its account with Bridge

**Option A (recommended — accurate through the current product direction):**

Zed will use its Bridge account in connection with its dollar-denominated consumer wallet product:

1. **Issuance/redemption orchestration:** facilitating the minting of stablecoins against USD and redemption of stablecoins to USD, with customer-destined stablecoins delivered directly to customers' self-custodied wallets (Zed never holds customer assets);
2. **Corporate treasury:** funding, holding, and converting between USD and stablecoins on Zed's own account to support product operations (e.g., operational float, fees); and
3. **Operational payments** related to the above.

All customer-facing activity involves Philippine-resident retail customers who have passed Zed's KYC; all Bridge-account activity is initiated by Zed on its own corporate behalf.

**Option B (narrower, if you prefer treasury-only scope):**

Zed will use its Bridge account for corporate treasury purposes on its own behalf: converting between USD and stablecoins, holding stablecoin balances, and funding operational flows for its dollar-denominated consumer product. Customer assets are self-custodied and do not transit Zed's Bridge account.

## 5. Primary countries of operation

Zed Financial, Inc. is incorporated in [Delaware, USA / the Philippines — confirm entity jurisdiction]. All of our operations, employees, and customers are in the **Philippines**; it is the only market we serve. [If a US parent/sub structure exists: operations are conducted in the Philippines through [entity]; the Bridge account will be held by [entity].]

---

> **Send-checklist (don't paste):** fill every `[...]`; attach the two Q2 artifacts + the Q3 certificates; delete Option A or B in Q4; confirm the jurisdiction line in Q5 matches the entity under review (Customer ID 9619036d-89d4-4e5e-8df2-118d9aeee9fd, steve@zed.co).

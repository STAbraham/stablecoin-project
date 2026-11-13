<!-- Processed 2026-11-12 from inbox/. Per Steve: brought into the PRD as CONTEXT ONLY, not definitive —
     this is a research handoff, not a legal opinion; the PRD's W-Q3/W-Q4 counsel gates remain the deciding items.
     PRD propagation: tracks/d-wallet-first/prd.md §5.0 + W-Q3/W-Q4/W-R11. -->

# USDC / USDT in the Philippines
## Securities classification, yield, rewards, and operating-model implications

**Project:** Zed investment / stablecoin research  
**Prepared:** November 12, 2026  
**Status:** Research handoff for product, compliance, and Philippine legal counsel; not a legal opinion or authorization to launch.  
**Scope:** Ordinary USDC and USDT holdings, services involving those tokens, and hypothetical yield or rewards programs. This file deliberately excludes the broader foreign-equity platform analysis, Qualified Buyer registrar requirements, and registrar penalties.

---

## 1. Starting conclusion and level of certainty

**Working interpretation:** The strongest argument for ordinary, non-yield-bearing payment stablecoins avoiding Philippine securities registration is that the relevant instrument or transaction is **not a security in the first place**. That differs from selling a security through a registration exemption. The Securities Regulation Code (SRC) and the SEC's crypto-asset rules require these questions to be distinguished. [S1, S5]

**Important uncertainty:** The materials reviewed did not establish a published Philippine SEC determination categorically resolving both USDC and USDT as non-securities for every Philippine offering. Their availability on a platform is not being treated here as proof of such a determination.

**Central product implication:** Analyze three things separately: the underlying token; the complete customer-facing investment or rewards arrangement; and the regulated activities performed by each provider. A defensible conclusion about the first does not decide the other two. [S1, S2, S5, S6]

**Recommended posture:** Treat a payment wallet and an investment/yield feature as separate legal workstreams, even when both use the same token. Do not assume a proposed partner, custody architecture, or Zed entity has already been approved.

## 2. Why the ordinary tokens have a non-security argument

### USDC: fixed-dollar value is different from participation in reserve earnings

Circle's non-EEA USDC terms, dated October 15, 2026, describe an intended value of USD 1 and conditional redemption at that amount. They expressly deny holders entitlement to reserve interest or investment returns and state that USDC itself does not generate a return. Direct redemption requires an eligible, registered Circle Mint account; merely possessing USDC is not enough. [S3]

**Interpretation:** Circle's investment of reserve assets does not, by itself, make a USDC holder a participant in the reserve portfolio's profits. The contractual entitlement is the important distinction. A third party promising a return on USDC introduces a different arrangement that must be examined separately.

### USDT: assess its own terms rather than assuming equivalence with USDC

Tether's terms, dated February 26, 2026, describe USD-pegged issuance and redemption, verification requirements, fees, minimums, and other conditions. They describe reserves as including cash, cash equivalents, and other assets, potentially including affiliate loan receivables. The reviewed terms frame the basic product around pegged redemption rather than participation in reserve performance. [S4]

**Interpretation:** USDT supports a similar payment-token argument, but USDT and USDC should not be treated as identical contracts or identical reserve exposures. Confirm the actual issuer, supported network, redemption route, and customer rights for each proposed integration.

### Philippine investment-contract test

In *Power Homes Unlimited Corp. v. SEC*, the Supreme Court applied an investment-contract test involving money invested in a common enterprise with expected profits primarily from others' efforts. This examines the arrangement's substance, not just its name. [S2]

**Application:** Acquiring dollar-denominated value for storage or transfer is different from contributing assets to a managed arrangement promising investment returns. Expecting the dollar's peso value to rise does not, by itself, establish all elements of that test; a managed FX-return promise would require a separate analysis.

**Qualification:** Lack of yield is not a complete exclusion from securities law. SRC Section 3.1 also includes notes, evidences of indebtedness, participation interests, and other instruments. Counsel must test those categories rather than stopping at the investment-contract analysis. [S1]

## 3. What yield changes

The relevant contrast is between these hypothetical propositions:

> **Payment proposition:** Hold or transfer USDC/USDT, with no investment return promised by the platform.
>
> **Investment proposition:** Commit USDC/USDT to an arrangement that generates or promises a financial return.

The latter may create a separate investment contract, debt obligation, participation interest, or other regulated product. That does **not** require concluding that every USDC or USDT token everywhere has become a security. The agreement, rights, fund use, and marketing can be the relevant subject of classification. [S1, S2]

The funding source matters, but it is not a standalone answer. A contractual return funded from an operator's general revenue deserves review even when customer assets are not lent out. Conversely, an ordinary purchase rebate should not automatically be equated with investment income simply because it is paid in USDC. *SEC v. Prosperity.Com* illustrates the importance of distinguishing genuine commercial incentives from investment returns; it is not a stablecoin-rewards safe harbor. [S11]

**Analytical cautions:** A fixed rather than variable rate, payment in additional tokens, a discretionary label, or withdrawal on demand does not independently resolve classification. Neither does moving the promise to a third-party partner. Evaluate the complete arrangement and each participant's actual role. These are research interpretations, not published Philippine rulings on the hypothetical products below.

## 4. Yield and rewards scenario matrix

**All assessments below are preliminary interpretations for product triage, not formal regulatory categories or approvals.** Apply the legal tests above to the actual contracts and customer journey. [S1, S2, S11]

| Hypothetical model | Preliminary assessment | Decisive facts to establish |
|---|---|---|
| **Plain USDC/USDT holding and transfers; no promised return** | Strongest payment-token/non-security argument. Still requires an operating-model review. | Customer entitlement, custody, redemption access, and platform activities. |
| **Cashback or a purchase-linked rebate paid in USDC/USDT** | More distinguishable from investing capital for a return. Not automatically outside crypto marketing or consumer-protection rules. | Is the benefit genuinely tied to a purchase, rather than balance size or holding duration? |
| **A promotional payment calculated as a percentage of wallet balance over time** | Material classification uncertainty even when paid from a marketing budget and assets remain idle. | Contractual promise, duration, balance requirement, customer inducement, and use of funds. |
| **Issuer or intermediary shares reserve income with holders** | Weakens the central argument that holders receive fixed-dollar value without reserve investment participation. | Enforceable profit rights, portfolio exposure, and whether an additional instrument is issued. |
| **Customers lend stablecoins to an operator for a fixed return** | Significant securities/debt and potentially other financial-regulatory issues. | Who borrows, repayment obligations, pooled financing, security for repayment, and loss allocation. |
| **Managed lending or investment vault; returns accrue to users** | Significant investment-contract or participation-interest issues. | Who selects investments, controls assets, bears losses, and issues any receipt or claim. |
| **Self-custody wallet with integrated access to an offshore yield service** | Self-custody does not answer the separate questions about promotion, intermediation, or investment rights. | Actual key control, transaction authority, referral compensation, provider permissions, and retail access. |

**Working design comparison:** A modest purchase-linked rebate paid from business revenue is analytically easier to distinguish from a yield product than a standing promise to pay a percentage on stored balances. This is a relative assessment, not a recommendation to relabel yield as cashback.

## 5. Regulation that remains relevant without securities registration

### A. BSP virtual-asset services

BSP Circular 1108 covers specified exchange, transfer, and safekeeping/administration activities for others, treats VASPs as money-service businesses, and sets authorization, risk-management, AML, and consumer-protection requirements. It separately excludes specified issuer-offering financial services within SEC jurisdiction. [S6]

**Implementation consequence:** Create an entity-by-entity map of fiat collection, conversion, transfer, custody, and redemption. Do not assume that outsourcing one activity authorizes all of Zed's remaining activities.

### B. SEC offering and marketing requirements

SEC MC 4 (2025) distinguishes general crypto-asset disclosure from securities registration. Section 5 ordinarily requires filing and publishing a disclosure document at least 30 days before marketing or offering, subject to exceptions. Section 6 addresses crypto-asset securities. Section 5.5.3 concerns offerings within other Philippine regulators' purview; it is not a blanket exemption from securities law. Section 7 separately regulates marketing. [S5]

**Question for counsel:** Which requirements apply to the specific offeror, distributor, and customer journey, and what is the precise basis for any exception?

### C. Token due diligence and ongoing review

BSP Memorandum M-2026-023, dated June 5, 2026, addresses token-listing diligence, including reserves, redemption, liquidity, and legal rights. It requires ongoing monitoring and delisting triggers, and expressly recognizes that securities and SEC CASP requirements may apply when a token is deemed or offered as a security product. [S7]

**Implementation consequence:** Evaluate each token and supported network rather than approving a ticker in the abstract. Define what happens if terms, reserves, liquidity, or legal treatment change.

### D. Offshore counterparties and Philippine retail access

BSP Memorandum M-2026-003 addresses BSP-supervised financial institutions' dealings with virtual-asset providers. It permits specified licensed offshore counterparties, but separately states that direct access by Philippine-resident retail customers to offshore VASPs is not allowed unless those providers are registered with BSP or SEC. [S8]

**Scope caution:** This memorandum is addressed to BSP-supervised institutions. Do not convert it into an unsupported claim that mere individual ownership of an offshore-issued token is unlawful. For a Zed-linked distribution or funds-flow arrangement, however, its application requires explicit review.

### E. Licensing availability

BSP Memorandum M-2025-031 continued the moratorium on new VASP licenses from September 1, 2025, subject to reassessment. [S9]

**Open implementation item:** Confirm the moratorium's current application, any later changes or exceptions, and the exact permissions of a proposed partner before assuming a new standalone license is available.

### F. Consumer protection

The Financial Products and Services Consumer Protection Act addresses fair treatment, disclosure, customer assets, complaints, and provider responsibilities across financial products and services. Non-security classification does not remove this separate regime where applicable. [S10]

**Recommended disclosures:** Distinguish token value from investment return; identify who owes repayment; explain depeg, issuer, custody, liquidity, and withdrawal risks; and substantiate any insurance or guarantee claim. Do not imply that a token balance is an insured bank deposit merely because it is dollar-denominated.

## 6. Product facts to resolve before a legal conclusion

The following is a proposed diligence checklist, not a description of an already selected Zed architecture.

**Customer entitlement.** Does the customer own native USDC/USDT, hold a custodial entitlement, lend assets to someone, or receive a different receipt token? Who is legally obligated to return principal or pay rewards?

**Asset control.** Who controls keys, recovery, signing, freezes, and withdrawals? Can any provider deploy, pledge, lend, or transfer customer assets? What rights survive that provider's insolvency?

**Return source.** Is the benefit a purchase rebate, general-revenue subsidy, reserve-income share, borrower interest, investment gain, or another mechanism? Produce an auditable explanation rather than relying on the label "rewards" or "staking."

**Return calculation.** Is payment linked to balance, time, portfolio performance, or spending? Is it promised, variable, discretionary, capped, or revocable? What happens when the funding source underperforms?

**Operating roles.** Identify the contracting entity, offeror, marketer, custodian, conversion provider, investment manager, and payment obligor. List relevant licenses and actual permitted activities, not just corporate registration numbers.

**Customer journey.** Preserve draft screens and contracts showing onboarding, conversion, yield enrollment, disclosures, withdrawal, and complaints. Identify default settings and whether yield requires a separate, informed election.

**Funds flow.** Show ownership and control at each step: customer funds -> conversion -> token acquisition -> storage or investment -> reward payment -> withdrawal. Include intermediaries, fees, and failure cases.

## 7. Questions for Philippine counsel / regulators

1. **Classification:** What is the legal basis for treating the proposed plain-token offering as a non-security, including review of debt and participation categories? Is a fact-specific SEC confirmation advisable?
2. **Yield or rewards:** For each proposed variant, what exactly is the instrument or arrangement being assessed? Which contractual or economic features change the result?
3. **Operating permissions:** Which entity needs which BSP or SEC permission? Does a partner's authorization cover the contemplated product and Zed's role, or only part of the service?
4. **Distribution and offshore access:** How do MC 4 Sections 5-7 and BSP M-2026-003 apply to the proposed customer journey? Which filings, approvals, or restrictions arise before marketing?
5. **Safeguarding and contingency:** What segregation, reconciliation, wind-down, and customer-redress arrangements are required? What changes trigger renewed legal review?

**Suggested first deliverable:** A short written classification and permissions memo for (a) plain holding/transfers, (b) purchase-linked rewards, and (c) balance-linked or investment-funded yield. Require separate conclusions for each rather than a single generic "stablecoin opinion."

## 8. Guardrails for the next researcher

Do not carry forward any of these as established conclusions:

- USDC and USDT have blanket Philippine SEC non-security approval.
- No interest, full backing, or a USD peg alone determines securities status.
- A BSP license, disclosure filing, or exchange listing authorizes every yield feature.
- Self-custody, an offshore issuer, or payment from a marketing budget automatically removes regulatory obligations.
- Calling investment income a reward changes the arrangement's legal substance.

US or other foreign classifications should not be substituted for Philippine authority. This handoff does not analyze US law, tax, accounting, a particular yield provider, or the full rules for banking, trust, lending, payments, or e-money activities. Those may require additional work once the design is fixed.

## 9. Source register and verification notes

Sources below were accessed during preparation. Regulatory provisions and issuer terms are distinguished from this handoff's hypothetical applications. This was targeted verification, not an exhaustive search for every amendment, enforcement action, or unpublished SEC interpretation. The SEC circular was reviewed as a reproduced primary document because direct access to its SEC page failed.

**[S1] Securities Regulation Code, Republic Act No. 8799.** Relevant: Sections 3.1, 8, 10, and 28. Foundational classification, registration, exemption, and intermediary framework.  
[Statutory text - Lawphil](https://lawphil.net/statutes/repacts/ra2000/ra_8799_2000.html)

**[S2] Power Homes Unlimited Corp. v. SEC, G.R. No. 164182, February 26, 2008.** Philippine investment-contract test and substance-based analysis. Not a stablecoin case.  
[Supreme Court decision - Lawphil](https://lawphil.net/judjuris/juri2008/feb2008/gr_164182_2008.html)

**[S3] Circle, USDC Terms.** Reviewed version: October 15, 2026; non-EEA holders. Relevant: Sections 1-2 and redemption/risk provisions. Evidence of contractual terms, not a Philippine regulatory determination.  
[Issuer terms](https://www.circle.com/legal/usdc-terms)

**[S4] Tether, Token Terms of Sale and Service.** Reviewed version: February 26, 2026. Relevant: Section 4.1, issuance, redemption, reserves, and eligibility. Evidence of contractual terms, not independent verification of reserves or Philippine authorization.  
[Issuer terms](https://tether.to/en/legal/?tab=terms)

**[S5] SEC Memorandum Circular No. 4, series of 2025, SEC CASP Rules.** Relevant: Sections 1.8, 2, 4-8; particularly 5.1, 5.5.3, and 6. Primary regulatory text reviewed through a third-party mirror; relevant pages visually checked.  
[SEC issuance page](https://www.sec.gov.ph/mc-2025/sec-mc-no-04-series-of-2025the-sec-rules-on-crypto-asset-service-providers-sec-casp-rules/) | [Reviewed PDF mirror](https://babylon2k.org/wp-content/uploads/2025/06/2025-SEC-MC-No.-4-S.-of-2025-The-SEC-Rules-on-Crypto-Asset-Service-Providers-SEC-CASP-Rules-2-1.pdf)

**[S6] BSP Circular No. 1108, series of 2021, Guidelines for VASPs.** Relevant: scope, covered services, authorization, AML, and operational requirements.  
[Official BSP PDF](https://www.bsp.gov.ph/Regulations/Issuances/2021/1108.pdf)

**[S7] BSP Memorandum M-2026-023, June 5, 2026, Coin/Token Listing Guidelines.** Relevant: ongoing monitoring and Annex A, especially pillars V-VI on reserves/redemption and legal compliance.  
[Official BSP PDF](https://www.bsp.gov.ph/Regulations/Issuances/2026/M-2026-023.pdf)

**[S8] BSP Memorandum M-2026-003, January 2026, Reminders on Sound Risk Management Practices when Dealing with VASPs.** Relevant: page 1, counterparties and retail access; addressed to BSP-supervised financial institutions.  
[Official BSP PDF](https://www.bsp.gov.ph/Regulations/Issuances/2026/M-2026-003.pdf)

**[S9] BSP Memorandum M-2025-031, August 29, 2025.** Continued enforcement of the moratorium on new VASP licenses, subject to reassessment. Current application must be confirmed for implementation.  
[Official BSP PDF](https://www.bsp.gov.ph/Regulations/Issuances/2025/M-2025-031.pdf)

**[S10] Financial Products and Services Consumer Protection Act, Republic Act No. 11765, May 6, 2022.** Relevant: Sections 2-6, 8, and 13.  
[Statutory text - Lawphil](https://lawphil.net/statutes/repacts/ra2022/ra_11765_2022.html)

**[S11] SEC v. Prosperity.Com, Inc., G.R. No. 164197, January 25, 2012.** Illustrates fact-specific differentiation of commercial incentives from investment-contract returns. Not a ruling approving stablecoin rewards.  
[Supreme Court decision - Lawphil](https://lawphil.net/judjuris/juri2012/jan2012/gr_164197_2012.html)

---

**Resume point:** Obtain the actual token, custody, rewards, and funds-flow specifications. Then resolve classification and operating permissions separately for each variant. The next task is not to re-establish that payment stablecoins can have a non-security argument; it is to determine whether the proposed customer arrangement preserves that argument and is otherwise lawfully offered.

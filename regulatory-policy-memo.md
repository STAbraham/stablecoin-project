# Stablecoin Wallet (OUSD): Regulatory Architecture & Policy Positioning

**Status:** CONFIDENTIAL — working draft (markdown port of `Zed_OUSD_Regulatory_Policy_Positioning_Memo.docx`, received 2026-08-28; the docx in `inbox/processed/` is the original)
**Date:** 2026-08-28
**Role in this repo:** the authoritative rationale behind PRD v5's architecture (D3–D6, D10–D12, R27–R34). The PRD states *what*; this memo states *why*. Confirmations that would change it are tracked in `counterparty-counsel-tracker.md`.

**Executive position.** The recommended architecture gives Zed a strong basis to argue that it should not require a BSP VASP or money-changing/FX authority for the OUSD Wallet. The remaining material licensing perimeter is the **SEC CASP regime**: Zed may be viewed as an offeror and/or crypto-asset intermediary even though it does not operate an exchange. The recommended path is to seek SEC interpretive confirmation and, if needed, targeted exemption or StratBox relief rather than build the product around a full CASP license.

## 1. Product and regulatory objective

Open-loop OUSD wallet embedded in the Zed app; OUSD held in user-owned Privy wallets; Bridge for issuance/orchestration; Netbank for PHP collection and disbursement. Store-of-value (and eventually payments) wallet — not a crypto trading venue, deposit account, or customer FX account.

- **Fixed counterparties:** Bridge (issuance/orchestration infrastructure); Privy (embedded self-custody).
- **Target regulatory outcome:** no separate BSP VASP, MC/FXD, EMI, or deposit-taking authority for Zed; no SEC CASP registration if interpretive/exemptive relief is available.
- **Core design principle:** regulated-looking functions should be *issuer activity*, *Zed own-account treasury*, *bank activity*, or *customer-controlled wallet activity* — never Zed acting as principal in a fiat/VA exchange or as custodian.

## 2. Recommended target architecture

### 2.1 On-ramp: primary OUSD issuance, not customer FX

1. Customer requests an OUSD issuance ("Add 100 OUSD"); confirmation identifies OUSD and the issuer/issuance program, shows the PHP amount required, and shows a Zed issuance/FX fee of zero.
2. Customer pays PHP to a dedicated Netbank collection VA — purchase/issuance consideration collected by Zed in its distributor/collection role. The customer never receives, owns, or has a claim to USD.
3. Zed funds issuance from pre-existing Zed-owned USD liquidity at Bridge (treasury assets, not a customer USD balance).
4. OUSD is minted by the issuer/issuance infrastructure directly to the customer-owned Privy wallet. OUSD must not pass through a Zed wallet.
5. Zed later rebalances treasury in aggregate — not matched as a customer-by-customer PHP-to-USD sale.

*Illustrative:* user requests 100 OUSD; Zed shows ₱5,850 due (reference rate, no spread); user pays the VA; Zed uses $100 of its Bridge settlement balance to cause a 100-OUSD mint direct to the user's address; day-end, Zed may convert aggregate PHP into USD to replenish its own liquidity. At no point does the user hold or become entitled to USD.

### 2.2 Wallet: genuinely self-custodied and open-loop

- User-owned under Privy's self-custodial configuration; **no Zed authorization key, signer, quorum position, or policy permitting unilateral movement or export** of user assets.
- User must be able to recover/export wallet control and use the wallet independently of Zed.
- Open-loop: customer may send/receive OUSD externally; the UI may simplify, but transfers remain customer-signed wallet actions.
- No Zed omnibus OUSD wallet; no internal ledger liability representing customer OUSD; on-chain balances are the source of truth.

### 2.3 PH off-ramp: direct issuer/Bridge redemption, then local fiat payout

1. Customer requests redemption; Zed creates/references a customer-attributed Bridge/Open Standard redemption route.
2. Customer signs from Privy **directly to the redemption/burn address** — customer OUSD must never transfer to a Zed-controlled address.
3. Bridge/issuance stack burns/redeems; USD settles to Zed's prefunded/settlement arrangement, attributed to the customer.
4. Zed/Netbank pays PHP from local liquidity to the customer's own PH bank account. Treasury rebalancing remains separate and aggregate.

Bridge's public Transfer API supports crypto→fiat transfers, customer-wallet sources, and `on_behalf_of`; liquidation addresses are documented. **OUSD-specific mint/burn behavior and settlement-to-prefunded remain counterparty-confirmation items** (tracker C-BR-7..10).

### 2.4 Rewards

- Working assumption: Open Standard pays Zed's partner **Marketing Fee on-chain in OUSD**, based on balances in registered wallets associated with Zed's direct customers. The fee is **Zed revenue**, not customer property awaiting distribution.
- Zed operates a **separate customer rewards program** ("Zed Rewards").
- **Preferred fulfillment:** Zed-owned reward economics/settlement value funds **incremental primary OUSD mints directly to each customer wallet**. Avoid routine Zed-payout-wallet → customer-wallet transfers if mint-based fulfillment is supported.
- Customer terms must not create a contractual right to Open Standard's Marketing Fee. Marketing says "variable Zed Rewards," never "your OUSD earns Treasury interest/yield."

## 3. BSP VASP analysis

BSP Circular 1206 (s. 2024) consolidated MSB/VASP rules into the M-Regulations. VASP scope **expressly excludes** (a) participation in / provision of financial services related to an *issuer's offer and/or sale* of a virtual asset, and (b) entities acting *solely on their own behalf*. The structure is designed around those boundaries.

| VASP limb | Zed position | Design facts supporting position |
|---|---|---|
| Fiat ↔ VA exchange | Strongest issue, but framed as issuer primary offer/sale | Primary OUSD issuance; no Zed inventory resale; zero issuance/FX economics; direct mint to user wallet |
| VA ↔ VA exchange | No | No USDC/other customer asset legs; any treasury digital asset is never attributed to customer balances |
| Transfer of VAs | Strong argument no for issuance/redemption; wallet transfers residual interpretive risk | Mint direct to customer; redemption direct to issuer/Bridge; Zed never receives customer OUSD; open-loop sends are customer-signed from self-custody |
| Safekeeping / administration / control | Strong argument no | User-owned Privy wallet; no Zed unilateral signer; export/recovery; no omnibus custody or internal OUSD liability ledger |

**Core BSP policy argument:** Zed is not operating a virtual-asset exchange or custodial wallet. It facilitates participation in the OUSD issuer's primary issuance and redemption, while customer OUSD is issued directly to and controlled solely by the customer. Zed's PHP/USD conversions are own-account treasury management, not customer FX. The response to the functional challenge ("user gives Zed PHP, receives OUSD") relies on the *scope carve-out for services connected to an issuer's offer/sale* — not semantic relabeling — so the facts must preserve genuine primary issuance: no Zed OUSD inventory, no secondary-market execution, no Zed spread.

**Offshore Bridge relationship (BSP M-2026-003):** BSFIs may deal with duly licensed/authorized offshore VASPs subject to due diligence, but **direct access by PH retail customers to offshore VASPs is not allowed** unless the provider is BSP/SEC-registered. Therefore: Bridge is Zed's offshore infrastructure/counterparty, never a foreign retail crypto app for Zed's users; Bridge end-user identifiers are KYC/compliance/attribution constructs only; confirm Bridge's US MSB/MTL or home-jurisdiction authorizations before launch and retain evidence (tracker C-BR-14).

## 4. FX / money-changing analysis

No customer PHP/USD transaction exists: the user is never credited USD, cannot withdraw USD, has no USD receivable; Zed quotes an all-in PHP amount for an issuance and earns no spread; corporate PHP/USD liquidity is managed separately.

- Do **not** display "PHP → USD," a Zed-sold FX rate, or an FX spread in the customer flow.
- Do **not** book a customer USD balance, payable, or sub-ledger entitlement.
- Treasury records aggregate corporate FX P&L internally — never characterized as customer FX revenue.
- **Prefer bank-executed PHP/USD treasury conversion. Coins.ph is not part of the base customer flow** merely to "insert a VASP."

**Working conclusion:** strong argument Zed provides no standalone money-changing/FX-dealing service — a structural conclusion, not a naming convention.

## 5. SEC CASP analysis *(the principal unresolved licensing issue)*

SEC MC 4 (s. 2025) defines crypto-asset services to include **offering crypto-assets to the public** and **crypto-asset intermediation**; "offeror" includes agents/representatives of the issuer; order execution includes subscribing on behalf of clients; order transmission includes receiving and transmitting purchase orders.

| SEC question | Working assessment | Recommended posture |
|---|---|---|
| Is Zed an "offeror"? | **Material risk: yes** — PH-facing distributor, possibly agent/representative of the issuer | Don't rely on "not an exchange"; seek SEC confirmation / exemptive relief |
| Order transmission / execution? | Material risk — customer instruction flows through Zed to Bridge/issuer | Structure as narrow issuance distributor, zero trading/custody; seek registration exemption |
| Public-offering disclosure? | Likely relevant even if OUSD is not a security (MC 4 §5) | Coordinate issuer + Zed filing/relief; seek §5.5.4 exemption if appropriate |
| Full CASP registration? | Not preferred; disproportionate to the narrow model | Exemption under MC 5 if available; StratBox (MC 9, s. 2024) for pilot if needed |

**Strategy:** (1) interpretive confirmation first, on the narrow fact pattern (one third-party USD stablecoin; primary issuance/redemption only; no secondary trading; no custody; no spread; user-owned wallets; existing BSP supervision); (2) if treated as CASP, seek MC 5 registration exemption (50-user controlled pilot supports it); (3) address the offering-disclosure question separately; (4) StratBox as pilot fallback.

## 6. Securities / investment-contract analysis

Philippine Howey-style test (Power Homes v. SEC; SEC v. Prosperity.Com). **Working position:** OUSD itself is not a crypto-asset security if the holder's substantive right is 1:1 redemption and OUSD carries no entitlement to reserve income. **Key risk:** marketing "Treasury yield on your OUSD" makes profit expectation central to acquisition. **Mitigation:** Marketing Fee is Zed's; separate Zed Rewards terms; rewards variable and Zed-determined, never a token-embedded yield right. (A non-security crypto-asset can still be subject to the CASP Rules — this analysis does not resolve §5.)

## 7. E-money, deposit-taking, product characterization

No Zed monetary-value liability: the customer's asset is issuer-issued OUSD held on-chain, not a Zed-issued wallet balance — outside BSP's e-money definition (claim on issuer, issued against funds, redeemable). Avoid "deposit," "savings account," "USD account," "insured balance." Use "OUSD Wallet" / "Dollar Wallet"; disclose not-a-PH-bank-deposit, not PDIC-insured.

## 8. AML, consumer protection, remaining controls

- Existing KYC/AML and transaction-monitoring obligations continue; add crypto indicators to monitoring/case-management rules.
- Bridge/issuer attribution data aligned to Zed KYC without making Bridge a direct-access offshore retail platform.
- Open-loop exposure: screen wallet addresses/transactions; define unsupported-asset, high-risk, and sanctions handling (tracker C-INT-4).
- Disclosures: stablecoin/reserve risk, smart-contract/blockchain risk, self-custody/recovery, variable rewards, FX exposure of PHP value, no deposit insurance.

## 9. Facts the product must deliberately avoid

| Avoid | Why |
|---|---|
| Customer USD balances or entitlements | Creates an unnecessary customer FX/account product |
| Zed issuance or FX spread | Makes Zed look economically like a dealer/exchanger |
| Zed OUSD inventory sold to customers | Weakens primary-issuance / issuer-offer position |
| Customer OUSD sent to Zed for redemption | Creates a direct VA→fiat exchange fact pattern at Zed |
| Zed omnibus customer wallet | Creates custody/control and internal liability facts |
| Zed unilateral Privy signer | Undermines self-custody / no-control position |
| USDC as a customer-visible/intermediate entitlement | Creates avoidable VA→VA or outsourced-trading facts |
| "Guaranteed yield" / "Treasury interest" language | Raises securities and consumer-protection risk |

## 10. Working conclusions and action plan

| Regulatory perimeter | Working conclusion | Next action |
|---|---|---|
| BSP VASP | Strong argument no VASP authority needed if primary-issuance/redemption + self-custody facts preserved | Counsel opinion; optionally supervisory discussion with BSP |
| MC/FXD | Strong argument no customer FX service | Implement zero-spread issuance + aggregate own-account treasury |
| SEC CASP | **Material issue remains** | Interpretation; if needed, CASP registration exemption; StratBox for pilot |
| SEC crypto-asset offering | Likely relevant | Disclosure filing vs. §5.5.4 exemption |
| Crypto-asset security | OUSD not a security (working position); rewards must remain separate | Counsel Howey analysis; final marketing review |
| EMI/deposit-taking | Strong argument no, absent Zed-issued monetary liability | Wallet/stablecoin terminology + disclosures |
| AML/consumer protection | Applies | Extend controls; add wallet/blockchain monitoring + crypto disclosures |

**Bottom line.** The no-additional-BSP-license argument is strongest when the architecture is *operationally faithful to its legal characterization*. The main unresolved question is SEC CASP/offering treatment; seek narrow SEC relief rather than distort the product into a licensed-exchange model.

## Sources and authorities

- **BSP-1** BSP Circular No. 1206, s. 2024 — Consolidated MSB/M-Regulations — VASP scope, issuer-offer and own-account exclusions
- **BSP-2** BSP Memorandum No. M-2026-003 — Dealings with VASPs/offshore counterparties; prohibition on direct PH retail access to offshore VASPs unless locally registered
- **SEC-1** SEC MC No. 4, s. 2025 — CASP Rules — definitions, offeror, intermediation, offering disclosure + exemptions
- **SEC-2** SEC MC No. 5, s. 2025 — CASP Guidelines — registration framework; reported exemption authority
- **SEC-3** SEC MC No. 9, s. 2024 — StratBox — strategic sandbox relief
- **CASE-1** Power Homes Unlimited Corp. v. SEC, G.R. No. 164182 — PH investment-contract / Howey test
- **CASE-2** SEC v. Prosperity.Com, Inc., G.R. No. 164197 — application of the test
- **BRIDGE-1** Bridge — Prefunded Accounts (single developer-funded account, `on_behalf_of`)
- **BRIDGE-2** Bridge — Transfer API / one-time payments (crypto↔fiat, customer wallet sources)
- **BRIDGE-3** Bridge — Open Issuance (marketing/distribution rewards as newly minted tokens for Bridge-issued stablecoins)
- **PRIVY-1/2** Privy — self-custodial user wallets; wallet export
- **OUSD-1** Open Standard — OUSD open-loop positioning and partner economics
- **INTERNAL-1/2/3** Zed PRD v4; Zed↔Bridge email thread (through 8/16/26); OS partner-rewards screenshots (8/28/26)

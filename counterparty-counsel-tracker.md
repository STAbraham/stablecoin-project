# OUSD Counterparty & Counsel Open Questions Tracker

**Status:** Live — Phase 0 artifact. Markdown port (with stable IDs added) of `Zed_OUSD_Counterparty_Counsel_Open_Questions.docx` (2026-08-28, from the policy/architecture deep dive; original in `inbox/processed/`). Items marked *(added)* are Zed-side additions from the 8/28 Open Standard docs and ops needs; everything else is verbatim-in-substance from the docx.
**How to use:** the policy memo (`regulatory-policy-memo.md`) and PRD v5 intentionally proceed on working assumptions. This tracker is **the source of truth for closing them**. **Launch blocker** = must be confirmed before external customer launch; **Pilot blocker** = must be confirmed before any real-money external pilot.

Statuses: `Open` — no reliable answer yet · `Working assumption` — used in current architecture, unconfirmed · `Confirmed` — written answer / verified contract or API behavior, source linked · `Rejected` — answer contradicts assumption; **policy memo and PRD must be updated**.
**Source discipline:** every `Confirmed` gets a primary source (contract section, email, API doc URL + date, meeting note, written legal advice). Never close a launch blocker on oral recollection.

## 1. Bridge / Open Standard (owner: Steve ↔ Freddie)

| ID | Question | Why it matters | Working assumption | Gate | Status |
|---|---|---|---|---|---|
| C-BR-1 | **Legal OUSD issuer** — who is the legal issuer of OUSD and who owes the 1:1 redemption obligation? | Issuer identity drives the BSP issuer-offer argument, SEC offeror analysis, disclosures, counterparty diligence. | Bridge/OS issuance stack has an identified regulated issuer of record. | Launch blocker | Open |
| C-BR-2 | **Primary mint** — is each Zed end-user on-ramp a fresh primary mint rather than a transfer of existing inventory? | Central to the BSP issuer-offer/sale position. | Yes — primary issuance. | Pilot blocker | Open |
| C-BR-3 | **Direct mint address** — can a Zed-funded mint deliver OUSD directly to an arbitrary user-owned Privy address? | Avoids Zed receipt/custody/transfer of customer OUSD. | Yes. | Pilot blocker | Open |
| C-BR-4 | **Prefunded USD** — can one prefunded/master Zed USD balance fund multiple end-user mints? | Separates customer issuance from customer-specific FX. | Yes. | Pilot blocker | Open |
| C-BR-5 | **Customer attribution** — can every mint/redemption carry Bridge `customer_id`/`on_behalf_of` attribution while Zed remains the API customer/counterparty? | Compliance, reconciliation, BSP M-2026-003 posture. | Yes. | Pilot blocker | Open |
| C-BR-6 | **Retail relationship** — does Bridge require the PH end user to become a direct Bridge service customer, or can customer records be compliance/attribution records under Zed's relationship? | Direct PH retail access to offshore VASPs restricted (M-2026-003). | Bridge remains Zed infrastructure/counterparty; no direct retail interface. | Launch blocker | Open |
| C-BR-7 | **OUSD redemption route** — can OUSD be sent directly from the user's Privy wallet to an issuer/Bridge redemption/burn address? | Avoids customer OUSD touching Zed. | Yes. | Pilot blocker | Open |
| C-BR-8 | **Redemption settlement** — can USD redemption proceeds settle to Zed's prefunded/settlement account with the operation tied to the end user? | Enables local PH payout after issuer-side redemption. | Yes. | Pilot blocker | Open |
| C-BR-9 | **Liquidation address support** — does the generic liquidation-address / Transfer API support OUSD specifically, and on which chains? | Public docs are generic; OUSD-specific support not explicit. | OUSD has an equivalent direct redemption API. | Pilot blocker | Open |
| C-BR-10 | **Mint/burn chain semantics** — will on-chain activity show actual mint/burn rather than inventory transfers? | Supports factual primary-issuance/redemption characterization. | Mint/burn. | Launch blocker | Open |
| C-BR-11 | **Marketing Fee asset** — what token/currency is the monthly Network Partner Marketing Fee paid in? | Reward accounting and transfer design. | OUSD. | Pilot blocker | Working assumption |
| C-BR-12 | **Marketing Fee wallet** — can Zed designate a dedicated corporate payout wallet? Must it be Bridge/Privy-controlled? | Separates Zed revenue from customer assets. | Dedicated Zed corporate wallet. | Pilot blocker | Open |
| C-BR-13 | **Reward minting** — can Zed use earned value or prefunded USD to batch/incrementally mint reward OUSD directly to customer wallets? | Avoids recurring Zed→customer transfers (preferred Zed Rewards fulfillment). | Yes. | Launch blocker | Open |
| C-BR-14 | **Home-country licensing** — exact Bridge/issuer registrations/licenses covering the functions Zed uses? | M-2026-003 BSFI diligence on offshore counterparties. | Appropriately licensed/authorized in home jurisdiction. | Launch blocker | Open |
| C-BR-15 | **Terms / disclosures** — which issuer/Bridge terms and risk disclosures must Zed surface to end users? | SEC offering/consumer analysis; contractual allocation. | Issuer disclosures can be incorporated in Zed's flow without creating direct offshore retail access. | Launch blocker | Open |
| C-BR-16 | *(added)* **Chains + test cap** — OUSD supported chains (Base availability, per D6b) and whether the $500 entity-wide test cap can be raised for internal alpha. | Chain choice; week-3 alpha realism. | Base available; cap raisable. | Pilot blocker (chains) | Open |
| C-BR-17 | *(added)* **Immediate wallet registration** — path to register wallets with Open Standard now (dashboard API key "Sept 2026"; CSV interim?). Accrual is **not backdated** — every unregistered week is Marketing Fee permanently lost. | Marketing Fee accrual from day one (PRD §2a). | CSV upload via OS contact until API access. | Ops (pre-pilot) | Open |

## 2. Privy (owner: Steve)

**Sandbox status:** app created 2026-09-14 in the Privy dashboard — **App ID `cmsxvzv9e00ad0cjsiqvmxjha`** (shared with Privy contact per their onboarding ask). Dashboard exploration notes (Earn vault list, Treasury workspace, eligibility settings) land in `tracks/c-usdc-vasp-privy/research/` as Steve captures them.

| ID | Question | Why it matters | Working assumption | Gate | Status |
|---|---|---|---|---|---|
| C-PR-1 | **User ownership** — can wallets be configured so the user is the sole owner with exclusive owner permissions? | Self-custody / no-control analysis. | User is sole owner. | Pilot blocker | **Working assumption — docs-supported** (user-wallets docs, 9/14: "Users retain full custody... Neither Privy nor your application ever sees a user's private key"). Confirm our app's configuration — the platform also offers service-controlled accounts |
| C-PR-2 | **No Zed signer** — can the intended UX run without any server authorization key or signer capable of unilateral transactions? | Avoids custody/control characterization. | Yes. | Pilot blocker | **Working assumption — docs-supported** (user-wallets docs, 9/14: "Applications cannot transact without explicit user authorization"; TEE reconstitution "only with the user's explicit authorization"). Two residuals: (a) Moreta shows programmatic/sweep patterns exist — config must be locked; (b) reconstitution is gated on "a valid user access token from your authentication service," which Zed issues under BYO-auth — confirm token issuance ≠ transaction authorization |
| C-PR-3 | **Export / recovery** — can every user recover/export wallet control outside Zed? | Substantive self-custody; resilience if the Zed relationship ends. | Yes. | Pilot blocker | Open |
| C-PR-4 | **Open-loop send/receive** — can customers send to / receive from arbitrary OUSD addresses with user signature? | Open-loop wallet truthfulness (R32). | Yes. | Pilot blocker | Open — supportive: wallet-actions docs (9/14) show `transfer` as an authorization-signed wallet action on EVM/Solana |
| C-PR-5 | **Direct redemption signing** — can the user sign directly to a Bridge/OUSD redemption address from the embedded wallet? | Required off-ramp architecture (D6). | Yes. | Pilot blocker | Open |
| C-PR-6 | **Policy controls** — which optional policies can Zed apply *without* obtaining unilateral asset control? | AML/risk controls that don't undermine self-custody. | Only user-approved or non-custodial controls. | Launch blocker | Open — supportive evidence: deck + wallet-actions docs (9/14): per-action policy methods exist; caveat "Privy does not enforce policy rules for RPC methods... used implicitly by the wallet action" — need the concrete policy model |
| C-PR-7 | **External wallet interoperability** — practical user flow after export for the selected chain / smart-wallet model? | Must not claim portability that is only theoretical. | Usable with external wallet tooling. | Launch blocker | Open |

## 3. Netbank (owner: Steve)

| ID | Question | Why it matters | Working assumption | Gate | Status |
|---|---|---|---|---|---|
| C-NB-1 | **Dedicated collection VAs** — second purpose-dedicated VA per user under the existing arrangement? | Clean separation from card payment flows (D9a). | Yes. | Pilot blocker | Open |
| C-NB-2 | **Collections legal capacity** — can the stablecoin collection account be documented as purpose-specific collection/settlement rather than a customer deposit balance? | No-deposit/no-EMI and agency narrative. | Yes / suitable contractual language available. | Launch blocker | Open |
| C-NB-3 | **PHP→USD treasury FX** — can Netbank execute corporate PHP/USD conversions for Zed? Accounts/limits/docs required? | **Removes the need for Coins.ph in the base flow** (D10). | Yes. | Pilot blocker | Open |
| C-NB-4 | **USD outbound funding** — can USD move from Zed/Netbank to the Bridge settlement/prefunded arrangement with acceptable timing/cost? | Operational treasury path. | Yes. | Pilot blocker | Open |
| C-NB-5 | **Disburse-to-Account** — production scope, sandbox/credentials, limits, InstaPay/PESONet behavior. | PH payout rail (D9b). | Enabled. | Pilot blocker | Open |
| C-NB-6 | **USD→PHP settlement support** — can Netbank receive USD redemption settlement and execute corporate conversion before PHP payout? | Further separates local fiat conversion from customer redemption. | Prefer yes. | Launch blocker | Open |
| C-NB-7 | **Account segregation** — can stablecoin collection and payout floats be operationally segregated from general/card funds? | Reconciliation and agency characterization. | Yes. | Pilot blocker | Open |

## 4. Philippine counsel / Compliance (owner: Open Question #8 — unassigned)

| ID | Question | Why it matters | Working assumption | Gate | Status |
|---|---|---|---|---|---|
| C-LC-1 | **BSP issuer-offer exclusion** — does Zed's distributor/collection/settlement role fall within the M-Regulations exclusion for services related to an issuer's offer/sale? | Core no-VASP thesis. | Yes, if primary-issuance facts are preserved. | Launch blocker | Open |
| C-LC-2 | **Open-loop wallet transfers** — does UI for user-signed sends/receives make Zed a VASP "transfer" provider despite no custody/control? | Residual VASP limb. | No, if Zed is purely wallet software and the user controls signing. | Launch blocker | Open |
| C-LC-3 | **Issuer redemption** — treatment of direct issuer redemption under BSP rules (which mention issuer offer/sale but not redemption)? | Core off-ramp thesis. | Redemption is issuer-side activity; Zed handles only downstream fiat settlement. | Launch blocker | Open |
| C-LC-4 | **FX / MC-FXD** — does zero-spread, no-customer-USD, aggregate-treasury design keep Zed outside customer FX dealing? | Avoid separate FX authority. | Yes. | Launch blocker | Open |
| C-LC-5 | **BSP M-2026-003** — does Bridge `customer_id`/KYC attribution *without* a direct retail interface avoid prohibited "direct access" to an offshore VASP? | Bridge is not PH-registered. Bears on D11 (US/EU off-ramp) too. | Yes, if Bridge remains Zed counterparty/infrastructure. | Launch blocker | Open |
| C-LC-6 | **SEC CASP classification** — is Zed an offeror, order transmitter/executor, or other CASP under MC 4? | Principal remaining licensing perimeter. | Material risk; seek SEC confirmation. | Launch blocker | Open |
| C-LC-7 | **CASP registration exemption** — process, timing, evidentiary standard for MC 5 exemption? | Preferred no-full-license path. | Available and appropriate for the narrow pilot/model. | Launch blocker | Open |
| C-LC-8 | **Crypto-asset offering** — who files the MC 4 §5 disclosure, or can OUSD/Zed obtain §5.5.4 relief? | Separate from CASP registration. | Issuer/Zed coordinated path needed. | Launch blocker | Open |
| C-LC-9 | **StratBox** — would SEC StratBox permit pilot testing with relief while exemption/interpretation is pending? | Pilot fallback. | Potentially yes. | Pilot blocker | Open |
| C-LC-10 | **OUSD as security** — does OUSD satisfy any SRC security/investment-contract test? | Would trigger separate registration requirements. | No, assuming 1:1 redemption and no token-level yield right. | Launch blocker | Open |
| C-LC-11 | **Zed Rewards** — does a separate variable rewards program change the OUSD security analysis or create another regulated product? | Marketing/rewards risk. | No, if clearly discretionary/separate and not a token entitlement. | Launch blocker | Open |
| C-LC-12 | **EMI / deposit-taking** — does the product create any Zed monetary-value liability or deposit-like relationship? | Avoid EMI/deposit licensing. | No. | Launch blocker | Open |
| C-LC-13 | **FCPA / disclosures** — specific crypto financial-consumer disclosures and suitability requirements applying to Zed? | Consumer compliance. | Applies; build into launch checklist. | Launch blocker | Open |
| C-LC-14 | **AMLC status / obligations** — does SEC CASP/offer activity change Zed's covered-person registration or AML program obligations beyond the existing BSFI framework? | Compliance implementation. | Needs confirmation. | Launch blocker | Open |

## 5. Internal decisions / artifacts (owner: Steve)

| ID | Decision | Description | Due |
|---|---|---|---|
| C-INT-1 | Final product name | OUSD Wallet / Dollar Wallet naming avoiding deposit-account implication (PRD Open Question #9, D12). | Before UX copy lock |
| C-INT-2 | Reference rate policy | Transparent FX reference source + quote-window policy; zero Zed issuance spread (PRD Open Question #2). | Before pilot |
| C-INT-3 | Rewards formula | Zed Rewards share, cadence, minimum balance, disclosure — after Marketing Fee mechanics confirmed (PRD Open Question #1). | Before external launch |
| C-INT-4 | Wallet screening policy | Treatment of external inbound/outbound OUSD, sanctions/high-risk addresses, unsupported assets sent to the address. | Before external launch |
| C-INT-5 | Regulatory engagement sequence | Informal SEC/BSP meeting vs. written interpretive request vs. exemption vs. StratBox application — ordering. | Before external launch |
| C-INT-6 | *(added)* Accounting treatment | Confirm booking: Marketing Fee as Zed revenue; Zed Rewards as program expense/liability. | Before external launch |

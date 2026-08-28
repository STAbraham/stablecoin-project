**ZED FINANCIAL**

OUSD PRD Handoff: Regulatory Architecture Decisions

Instructions for updating “Zed Dollar Account (OUSD) - Product Requirements Document” from Draft v4

| **Status** | CONFIDENTIAL - WORKING DRAFT |
|------------|------------------------------|
| **Date**   | 28 August 2026               |

| **Purpose.** Use this memo as the authoritative handoff for revising the existing OUSD PRD. Preserve the commercial product goals and the fixed Bridge + Privy counterparties, but update the money flows, wallet model, terminology, rewards, and compliance gates to reflect the new regulatory architecture. |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

# 1. What is unchanged

- OUSD remains the pilot stablecoin; Bridge remains the issuance/orchestration integration; Privy remains the embedded-wallet provider.

- Pilot remains focused on existing Zed cardholders and begins at small controlled scale.

- Dedicated per-user Netbank virtual collection accounts remain the preferred PHP funding rail.

- Netbank remains the preferred Philippine disbursement rail.

- User OUSD balances remain on-chain and are not Zed ledger liabilities; the internal ledger covers Zed-controlled funds and in-flight operations only.

- Operational requirements for dual control, reconciliation, runbooks, alerts, and zero-loss handling remain valid.

# 2. Architecture decisions that supersede PRD v4

| **Decision**             | **New instruction**                                                                                                                                      | **Supersedes / changes**                                                    |
|--------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------|
| On-ramp characterization | Customer requests primary issuance of OUSD for a PHP amount due; Zed acts as distributor/collection/settlement agent.                                    | D4 and §6.2 language that “Zed converts to USD and acquires OUSD.”          |
| Issuance economics       | Zero Zed spread and zero Zed issuance/FX fee.                                                                                                            | T3 and Open Question \#4 as presently written.                              |
| Treasury                 | Fund customer issuance from pre-existing Zed-owned USD liquidity; rebalance aggregate PHP/USD later.                                                     | D10 wording that can imply customer-specific FX.                            |
| Coins.ph                 | Remove from base architecture. Use only if later required as a regulated fallback or treasury venue.                                                     | D8/D10 references treating Coins as expected FX venue.                      |
| Mint path                | Require primary mint directly to customer Privy address; no Zed OUSD wallet in the customer path.                                                        | Any “acquire OUSD” implementation that could use inventory/resale.          |
| Wallet model             | Make Privy wallet genuinely user-owned, exportable/recoverable, and open-loop.                                                                           | §3 non-goal \#2 and §8 “closed-loop is product-enforced.”                   |
| Zed wallet controls      | No Zed unilateral signer, owner, or export capability.                                                                                                   | Any proposed policies/delegation that allow Zed to move customer assets.    |
| PH off-ramp              | Customer signs OUSD directly to Bridge/OUSD redemption infrastructure; Zed never receives customer OUSD. Local PHP payout follows redemption settlement. | §6.4 flow to “Zed’s redemption address.”                                    |
| Rewards                  | Treat Open Standard payment as Zed Marketing Fee; separate Zed Rewards program; prefer direct issuer mint of reward OUSD to users.                       | D5 / §6.3 pass-through “yield” framing.                                     |
| Product terminology      | Use OUSD Wallet / Dollar Wallet; avoid deposit/savings-account framing and customer FX language.                                                         | Summary / “Dollar Account” naming where it implies deposit or fiat account. |

# 3. Replacement on-ramp flow

1.  **Quote/request.** User selects the amount of OUSD to add (e.g., 100 OUSD). Zed shows the PHP amount required using a transparent reference rate and zero Zed issuance/FX fee.

2.  **PHP collection.** User sends PHP to the stablecoin-dedicated Netbank virtual account. Incoming-payment matching identifies the funding intent.

3.  **Issuance funding.** After payment match, Zed uses pre-existing Zed-owned USD liquidity in the Bridge settlement/prefunded arrangement. Do not create a user USD balance or customer-specific USD entitlement.

4.  **Primary mint.** Bridge/OUSD issuance infrastructure mints OUSD directly to the customer’s Privy address. Record issuer/Bridge transaction ID and on-chain mint hash.

5.  **Treasury rebalance.** Separately, ops/treasury periodically converts aggregate Zed-owned PHP into USD to replenish the Bridge settlement balance.

| **Ledger consequence.** Replace per-operation “customer PHP -\> customer USD” concepts with (a) PHP issuance consideration received, (b) Zed USD settlement asset consumed, (c) issuance completed to customer wallet, and (d) separate treasury rebalance entries. User OUSD remains off-ledger/on-chain. |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

# 4. Replacement wallet model

- Provision user-owned Privy wallet configuration. The user is the wallet owner.

- Do not configure a Zed authorization key or signer that can unilaterally transact, change owners/signers/policies, or export keys.

- Provide a recovery/export path that allows the user to use the wallet independently of Zed.

- OUSD is open-loop. Add send and receive capability to the product roadmap; all sends must be explicitly user-signed.

- Remove the “ignore unsolicited external deposits” concept. On-chain balance is the source of truth, so externally received OUSD should appear in the wallet balance subject to compliance screening/UX policies.

- No Zed omnibus OUSD custody account and no internal customer OUSD liability ledger.

# 5. Replacement PH off-ramp flow

6.  **User selects PHP withdrawal amount.** Show estimated PHP proceeds and any disclosed local rail fee; do not describe the service as Zed buying OUSD.

7.  **Create customer-attributed redemption route.** Use Bridge/OUSD redemption tooling or a customer-specific liquidation/redemption address tied to the Bridge customer/on_behalf_of identifier.

8.  **User signs OUSD directly to redemption infrastructure.** The source is the customer Privy wallet; destination is Bridge/OUSD issuer infrastructure, never a Zed wallet.

9.  **Bridge/OUSD issuer redeems/burns OUSD.** USD proceeds settle into Zed’s settlement/prefunded arrangement and remain attributable to the relevant redemption operation.

10. **Zed pays PHP locally.** Use the Netbank Disburse-to-Account API to pay the user’s own Philippine bank account from Zed’s PHP liquidity.

11. **Treasury rebalances separately.** Net aggregate USD/PHP exposure later; do not book a customer-specific USD/PHP trade.

| **Phase 0 gate.** Public Bridge docs support crypto-\>fiat transfers, customer wallet sources, on_behalf_of, and liquidation addresses, but OUSD-specific direct mint/burn behavior must be confirmed. If the direct redemption pattern is not supported, do not revert to “customer -\> Zed OUSD wallet.” Escalate to the fallback decision: licensed PH VASP off-ramp or defer PH off-ramp. |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

# 6. Rewards rewrite

- Working assumption: Open Standard pays Zed’s Network Partner Marketing Fee on-chain in OUSD.

- Qualifying customer wallets are registered/attributed to Zed for reward calculation even though the wallets are user-owned.

- Book the Open Standard payment as Zed revenue (subject to accounting confirmation), not as customer OUSD held in custody.

- Create separate “Zed Rewards” program terms and accrual logic. Do not state that the customer owns Open Standard’s Marketing Fee.

- Preferred fulfillment: fund incremental OUSD primary mints directly to customer Privy wallets. Keep Zed payout-wallet -\> user-wallet transfers as a fallback requiring legal sign-off.

- UI language: “variable Zed Rewards” or equivalent. Avoid “interest,” “Treasury yield owed to you,” or guaranteed APY language without legal approval.

# 7. Terminology and UX changes

| **Replace / avoid**         | **Use instead**                                                 |
|-----------------------------|-----------------------------------------------------------------|
| “Convert PHP to USD”        | “Add OUSD” / “Request OUSD issuance”                            |
| “FX spread”                 | No Zed spread; show PHP amount due / transparent reference rate |
| “USD balance”               | “OUSD balance”                                                  |
| “Zed holds your dollars”    | “Your OUSD is held in your self-custodied wallet”               |
| “Deposit / savings account” | “OUSD Wallet” / “Dollar Wallet” pending final compliance naming |
| “Closed loop”               | “Open-loop self-custodied wallet”                               |
| “Zed redemption address”    | “Issuer/Bridge redemption route”                                |
| “OUSD earns Treasury yield” | “Eligible OUSD may receive variable Zed Rewards”                |

# 8. Specific PRD sections to update

| **PRD section**       | **Required edit**                                                                                                               |
|-----------------------|---------------------------------------------------------------------------------------------------------------------------------|
| §1 Summary / Why OUSD | Rewrite PHP leg as issuance distribution + own-account treasury; remove “Zed converts to USD.”                                  |
| §3 Non-goals          | Remove external-transfer prohibition. Keep trading in other assets out of MVP, but make OUSD wallet open-loop.                  |
| D3 Custody            | Strengthen to user-owned Privy wallet, no Zed unilateral signing/export.                                                        |
| D4 On-ramp            | Replace with primary issuance flow above.                                                                                       |
| D5 Rewards            | Replace “yield pass-through” with Network Partner Marketing Fee + separate Zed Rewards.                                         |
| D6 Off-ramp           | Require direct issuer/Bridge redemption from user wallet; no Zed OUSD receipt.                                                  |
| D8 Backend            | Remove Coins.ph as expected customer-path venue. Keep only as optional treasury/fallback adapter.                               |
| D10 Treasury/FX       | Rewrite as pre-funded USD + aggregate own-account rebalancing; zero customer issuance spread.                                   |
| §6.2 On-ramp          | Replace end-to-end steps and R6 ledger fields.                                                                                  |
| §6.3 Rewards          | Rewrite attribution, accounting, and mint-based reward fulfillment.                                                             |
| §6.4 PH off-ramp      | Replace Zed redemption address flow.                                                                                            |
| §6.5 US/EU off-ramp   | Re-evaluate against BSP M-2026-003 offshore-access rule; Bridge remains Zed counterparty, not direct retail app.                |
| §6.8 Ledger           | Preserve user-balances-not-liabilities principle; revise in-flight accounts to match issuance/redemption settlement.            |
| §7 Treasury           | Remove customer-specific FX and FX spread. Retain float thresholds and dual control.                                            |
| §8 Compliance         | Replace closed-loop rationale with self-custody/open-loop controls; add SEC CASP/offering track and offshore-counterparty rule. |
| §10 Open questions    | Move partner/legal unknowns to Counterparty & Counsel Open Questions tracker and reference it as a Phase 0 artifact.            |

# 9. New hard requirements to add

- **R-New-1 - Primary issuance.** Customer on-ramps must settle as primary OUSD mint directly to the customer wallet; no Zed inventory resale without legal approval.

- **R-New-2 - No customer USD.** No database or ledger object may represent a customer USD entitlement or balance.

- **R-New-3 - Zero issuance economics.** Zed charges no spread/fee on PHP-to-OUSD issuance for the pilot.

- **R-New-4 - No Zed custody.** No customer OUSD may be held in a Zed-controlled wallet, including during on-ramp or redemption.

- **R-New-5 - User signing.** All outbound wallet transactions require user cryptographic authorization; Zed cannot unilaterally sign.

- **R-New-6 - Open-loop truthfulness.** External OUSD received by the wallet is recognized in the displayed on-chain balance; compliance controls may block in-app actions but must not falsify ownership/balance.

- **R-New-7 - Counterparty attribution.** Each mint/redemption is attributable to a Zed user in Bridge/OUSD systems without giving that user direct retail access to an offshore VASP interface.

- **R-New-8 - Regulatory gates.** External launch requires written sign-off on BSP VASP/FX posture and a resolved SEC path: no-action/interpretive confirmation, exemption, or StratBox relief.

# 10. Working assumptions to reference, not hard-code

- OUSD acquisition through Bridge is a true primary mint for each customer transaction.

- OUSD can be minted directly to an arbitrary customer-owned Privy address.

- OUSD can be redeemed/burned directly from the customer wallet without transferring to Zed.

- Redemption proceeds can settle to a Zed prefunded/settlement balance while remaining operation/customer-attributed.

- Open Standard Marketing Fee is paid on-chain in OUSD.

- Bridge can support reward-related incremental OUSD minting directly to end-user wallets.

- Bridge’s customer/on_behalf_of records are compliance/attribution constructs and do not constitute prohibited direct PH retail access to an offshore VASP.

| **Agent instruction.** When a working assumption affects implementation, preserve it as an explicit Phase 0 gate in the PRD. Do not silently convert it into a confirmed vendor capability. Use the separate Open Questions tracker as the source of truth for confirmation status. |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

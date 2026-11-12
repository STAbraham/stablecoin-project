# Coins.ph on-ramp suspended by the BSP — context for processing

**Drafted:** 2026-11-12 (Claude, from web research at Steve's request). Raw input for inbox processing — nothing below has been propagated into the PRD, integration doc, or tracker yet.

## What happened

- **2026-09-29:** Philippine Payments Management, Inc. (PPMI) issued **Advisory No. 2026-0929-029**, acting under **BSP Monetary Board Resolution No. 839**, ordering the **immediate partial suspension of DCPay Philippines, Inc.** (the operator behind Coins.ph) across the **InstaPay and PESONet** clearing houses.
- **Scope — suspended:** all **inbound** credit transfers to Coins.ph: cash-ins from banks (BDO, BPI, UnionBank, etc.) and e-wallets (GCash, Maya), personal QR Ph transfers, and inbound InstaPay for Business processing.
- **Scope — still operating:** **outbound** transfers (Coins.ph → external banks/e-wallets), core wallet features, and crypto services (trading, custody) under the separate VASP entity.
- **Status as of 2026-11-12:** the suspension has **not been lifted**; no public lifting conditions or duration were given. The advisory itself stated no reason, and the BSP has not published one.

## Entity structure (matters for us)

Coins.ph is one consumer brand over two BSP-regulated entities:

| Entity | License | Status |
|---|---|---|
| **DCPay Philippines, Inc.** | Electronic Money Issuer (EMI) — fiat peso wallets, domestic transfer rails | **Suspended inbound** (the entity named in the order) |
| **Betur, Inc.** | Virtual Asset Service Provider (VASP) — crypto trading, wallets, custody | Operating; not named in the order |

The crypto side is structurally intact — but fiat cash-ins that *fund* crypto purchases ride DCPay's rails, so the practical effect is that **the PHP→crypto on-ramp is dead** while the suspension holds.

## Alleged cause (reported, not officially confirmed)

- Per CoinDesk reporting (cited by BitPinas): after earlier BSP crackdowns on offshore gaming, **restricted offshore gaming/gambling operators allegedly shifted transaction flows to Coins.ph**, using its crypto infrastructure — explicitly including **stablecoins (USDT and USDC)** — to process settlement payments with offshore partners.
- Reports say the BSP is weighing **severe punitive actions including potential license revocation**; it is not specified whether the VASP license is in scope.
- **Coins.ph's response:** denies knowingly serving offshore gaming firms; says all licenses remain active and customer funds are safe; describes the pause as implementing BSP-directed "enhancements to internal controls."

## Why this matters for this project (drafter's notes — for processing, not yet decisions)

1. **The suspended capability IS the Track C on-ramp.** C-D4's flow — user pays PHP via InstaPay (preferred) / PESONet into a per-user virtual account at Coins.ph — is exactly the inbound rail now blocked. While the suspension holds, the pilot's deposit leg does not exist. The off-ramp (PHP out) is technically unaffected.
2. **Entity question for the integration:** our virtual-account cash-in almost certainly rides DCPay's EMI rails (to confirm — adds an entity-level dimension to OQ-12's custody questions: *which Coins.ph entity holds unconverted customer PHP?*).
3. **Pattern-match risk, beyond the outage:** the alleged abuse — third parties converting PHP through Coins.ph into stablecoins delivered outward — is uncomfortably close in *shape* to our architecture (merchant pass-through KYC, PHP in, USDC delivered to self-custodied external wallets). Even after reinstatement: (a) Coins.ph's appetite and controls for exactly this kind of merchant flow may tighten sharply; (b) launching this product on a partner under active BSP remediation has obvious optics/counsel implications (C-R14, regulatory-posture discipline).
4. **Counterparty risk is no longer hypothetical:** license revocation is reportedly on the table. The single-VASP-partner dependency in Track C now has a live demonstration of its failure mode.
5. **Overtaken by events:** the OQ-1..16 outbound packet to Coins.ph tech contacts, sandbox plans, and the "~2 weeks to live" integration timeline all predate this; the next conversation with Coins.ph is relationship-level (status, timeline to reinstatement, their read on merchant-flow viability), not API-level.
6. **Items likely touched at processing time:** PRD §1/§2/C-D4/C-D15 (pilot timeline), §6.2 status board (whole OQ table context + a new OQ on suspension status/reinstatement), §6.5 next steps; integration doc status header; counterparty tracker (C-INT items); possibly a fresh look at parked alternatives (tracks A/B, other VASP partners) depending on Steve's read.

## Sources

| Date | Source | What it adds |
|---|---|---|
| 2026-10-01 | [Manila Bulletin](https://mb.com.ph/2026/10/01/coinsph-suspended-by-bsp-from-cash-ins-via-banks-e-wallets) | Initial report: cash-ins from banks/e-wallets blocked |
| 2026-10-01 | [Fintech News PH](https://fintechnews.ph/73758/e-wallets/bsp-suspends-coinsph-instapay-pesonet-transfers/) | MB Resolution No. 839; DCPay named; outbound unaffected |
| 2026-10-01 | [Bilyonaryo](https://bilyonaryo.com/bsp-blocks-coins-ph-cash-ins-via-banks-e-wallets/) | Scope incl. QR Ph personal transfers |
| ~2026-10-13 | [BitPinas — inbound freeze reportedly tied to gambling](https://bitpinas.com/feature/coins-ph-inbound-freeze-reportedly) | PPMI Advisory No. 2026-0929-029 (9/29); CoinDesk-reported offshore-gaming link incl. USDT/USDC settlement; license-revocation risk; DCPay/Betur split |
| 2026-10 | [BitPinas — Coins.ph statement to users](https://bitpinas.com/business/coins-ph-cash-in-statement/) | "Temporarily paused … to enhance internal controls"; funds safe |
| 2026-10 | [BitPinas — exclusive clarification](https://bitpinas.com/business/exclusive-coins-ph-clarifies/) | Coins.ph: all licenses active; denies offshore-gaming ties |
| 2026-10-14 | [Blockhead](https://www.blockhead.co/2026/10/14/coins-ph-faces-philippine-central-bank-action-over-alleged-links-to-offshore-gambling-firms/) | Central-bank action over alleged gambling links |
| 2026-11 (checked 11-12) | [Tech Pilipinas](https://techpilipinas.com/bsp-suspends-coins-ph-instapay-pesonet-transfers/), [Astig.ph](https://astig.ph/bsp-dcpay-coins-ph-inbound-instapay-pesonet-suspension-2026/) | Still in force; what still works |

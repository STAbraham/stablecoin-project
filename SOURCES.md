# Source ledger (bibliography)

Every piece of external context processed into this project gets a row here at processing time — including things that can't live in `inbox/` (Slack threads, live dashboards, calls, web pages). Newest first. Purpose: trace any decision back to what informed it. Files archived in `inbox/processed/` are noted; link = original source where one exists.

| Processed | Source | Type | Digested into | Informed |
|---|---|---|---|---|
| 2026-09-23 | [#coins-ph-zed Slack thread: on/off-ramp Q&A recap](https://zedfinancial.slack.com/archives/C09HS2FTGTG/p1789436387222499) (Coins.ph: lara.tan, shawn.dong; 9/14–9/21) | Slack thread | `tracks/c-usdc-vasp-privy/research/coinsph-integration.md` | Track C PRD (on-ramp/KYC/off-ramp), C-Q9 |
| 2026-09-23 | "Create Customer API Documentation (V2).pdf" (Slack file F0C2DP9PM4N, from shawn.dong@coins.ph) | PDF spec | **PENDING — not retrievable via API; needs manual drop into `inbox/`** | merchantCreateUser spec |
| 2026-09-16 | Privy dashboard sandbox — Earn vault selection screen (Steve's screenshot) | Screenshot (`inbox/processed/2026-09-16-privy-sandbox-earn-vaults.png`) | `privy-earn.md` (C-Q5 sandbox-verified) | Vault list, live APY/TVL, Track C economics |
| 2026-09-14 | Privy tech docs ×7: [security](https://docs.privy.io/security/overview), [JWT auth](https://docs.privy.io/authentication/user-authentication/jwt-based-auth/overview), [user wallets](https://docs.privy.io/wallets/overview/solutions/user-wallets), [wallet actions](https://docs.privy.io/wallets/actions/overview), [financial flows](https://docs.privy.io/financial-flows/overview), [gas](https://docs.privy.io/wallets/gas-and-asset-management/gas/overview), [controls](https://docs.privy.io/controls/dashboard/overview) (links via Privy contact) | Vendor docs | `privy-tech-docs.md` | C-PR-1/2/4/6 evidence, C-Q4, D7 auth, R19 mapping |
| 2026-09-14 | [Privy blog: Robinhood](https://privy.io/blog/bringing-global-financial-markets-onchain-with-robinhood) | Blog (screenshot archived) | `robinhood-earn-case-study.md` | Track C comparable, C-Q6/C-Q7 |
| 2026-09-14 | [Privy blog: Moreta](https://blog.privy.io/blog/cross-border-stablecoin-payments-via-qr-codes-with-moreta) | Blog (screenshot archived) | `moreta-case-study.md` | Track C thesis precedent, C-PR-2 caution |
| 2026-09-14 | Privy overview deck (DocSend d3qrnv8en3g8dfh3, 14 slides) | Sales deck (screenshots archived) | `privy-overview-deck.md` | Platform claims, yield comparables, DLUSD note |
| 2026-09-14 | [Pete's Slack DM: Privy links](https://zedfinancial.slack.com/archives/D02BM4DRJJK/p1787619579914429) (8/24) + Privy docs ×5 (Earn overview/setup/revenue-sharing, assets/webhooks, custom OAuth) | Slack DM + vendor docs | `privy-earn.md` (+ provenance note in `inbox/processed/`) | C-Q1/2/3/5, Track C economics |
| 2026-08-28 | Zed_OUSD_Regulatory_Policy_Positioning_Memo.docx (Steve's deep dive) | Internal memo (archived) | `regulatory-policy-memo.md` | PRD v5.1 §8, R27–R34 rationale |
| 2026-08-28 | Zed_OUSD_Counterparty_Counsel_Open_Questions.docx (Steve's deep dive) | Internal tracker (archived) | `counterparty-counsel-tracker.md` | All C-* confirmation items |
| 2026-08-28 | Zed_OUSD_PRD_Agent_Handoff.md (Steve's deep dive) | Internal handoff (archived) | PRD v5 (D3–D6, D10–D12 recast) | The v5 regulatory architecture |
| 2026-08-28 | OS "OUSD Rewards" DocSend (2 pp) + "Earning Equity" (3 pp) + "Supply Contribution Proposal" (3 pp) | Partner docs (screenshots archived) | PRD §2a | D5 mechanics, equity program, attribution |
| 2026-08-16 | Zed–Bridge email thread through 8/16 (Freddie Allen) | Email PDF (repo root) | PRD v2 changelog | D2 OUSD pivot, timelines, $500 cap |

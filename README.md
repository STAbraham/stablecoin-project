# Stablecoin project — working conventions

Docs for the Zed Dollar Wallet (OUSD) pilot. See `ousd-account-prd.md` (PRD, v5), `counterparty-counsel-tracker.md` (Phase 0 partner/legal confirmations — the source of truth for what's confirmed vs. assumed), `funds-flow-bridge-kyb.html`/`.pdf` (Bridge KYB handoff), and — once started — `tech-design.md`.

## How iteration works

1. **Drop raw inputs in `inbox/`** — email PDFs, call notes, screenshots, pasted Slack threads, anything. No formatting needed; a `.md` with three bullets from a Netbank call is fine. Name with a date if convenient (`2026-08-18-netbank-call.md`).
2. **Tell Claude "process the inbox"** (any session — the project conventions are in persistent memory). Claude reads each item, updates the PRD / tech design accordingly, appends a changelog entry, moves the item to `inbox/processed/`, and commits.
3. **Review by diff, not by re-reading.** Every doc change is a git commit. Ask Claude "what changed since I last read?" or run `git log --oneline` / `git diff <sha>` — the changelog entries at the top of each doc summarize the same thing in prose.

## Stable anchors (the interface for feedback)

- **Decisions:** D1–D12 in the PRD. To revisit one, reference it by ID ("Netbank says no second VA — reopen D9a").
- **Requirements:** R1–R34, T1–T5 in the PRD (R27–R34 are the v5 regulatory-architecture invariants).
- **Open questions:** PRD §10 holds *business* questions only. Partner-capability and legal confirmations live in `counterparty-counsel-tracker.md` with IDs like C-BR-1 ("Freddie confirmed C-BR-1: …").
- The tech design doc will carry the same discipline, plus per-section status tags: `VERIFIED` (checked against code/docs), `ASSUMED` (best guess, safe default), `PENDING <partner>` (blocked on an external answer) — so partner answers map directly to the sections they unblock.

## Current external dependencies (who owes what)

Detail + status per item in `counterparty-counsel-tracker.md`. Headlines:

- **Zed → Bridge:** complete KYB (gates OUSD sandbox access; funds-flow doc prepared 8/27).
- **Bridge (Freddie):** primary mint direct-to-customer-wallet (C-BR-1), direct redemption from customer wallet (C-BR-2), `on_behalf_of` attribution (C-BR-3), reward mints (C-BR-4), chains + test-cap raise (C-BR-5). C-BR-1/2 are load-bearing for the v5 architecture.
- **Open Standard:** user-wallet registration under the Relationship test (C-OS-1), Marketing Fee payout token/destination (C-OS-2), immediate wallet-registration path — accrual is not backdated (C-OS-3).
- **Netbank:** Disburse-to-Account scope + sandbox (C-NB-1); second VA per user (C-NB-2).
- **Privy:** user-owned wallet config with recovery/export and no Zed signer (C-PR-1); contract + sandbox (C-PR-2).
- **Counsel:** BSP VASP/FX posture (C-LC-1), SEC CASP/offering path (C-LC-2), BSP M-2026-003 offshore-access analysis (C-LC-3) — the R34 launch gates; only items that can block launch after the build is done.

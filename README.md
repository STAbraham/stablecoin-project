# Stablecoin project — working conventions

Docs for the Zed Dollar Wallet (OUSD) pilot. See `ousd-account-prd.md` (PRD, v5.1), `regulatory-policy-memo.md` (regulatory architecture rationale — the *why* behind D3–D6/D10–D12 and R27–R34), `counterparty-counsel-tracker.md` (Phase 0 partner/legal confirmations — the source of truth for what's confirmed vs. assumed, with pilot-blocker/launch-blocker gates), `funds-flow-bridge-kyb.html`/`.pdf` (Bridge KYB handoff), and — once started — `tech-design.md`.

## Parallel tracks (added 2026-09-14)

The project explores **three alternatives in parallel** alongside the incumbent (PRD v5.1) architecture: **A** OUSD+CASP, **B** OUSD+VASP, **C** USDC via VASP partner + Privy Earn. `tracks/TRACKS.md` is the comparison board and rulebook; each track has `tracks/<track>/track.md` (thesis, Mermaid architecture, track-scoped IDs like `C-Q7`) and `research/` for track-exclusive digests; **cross-track or incumbent-relevant topics digest into root `research/`** (e.g., `research/privy-platform.md`, which also feeds tracker C-PR items). Digests are per **topic**, not per source doc — one doc can feed several, split by relevance (Privy platform sections → shared; Privy Earn sections → Track C). Route inbox items via `inbox/track-a|b|c/` or a filename prefix (`c-…`) as a hint; content always lands wherever it's relevant. The digest is the grok artifact the docs reference. Track lifecycle: exploring → candidate (gets a branded funds-flow diagram) → selected (merges into the PRD) / parked (with post-mortem).

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
- **Bridge / Open Standard (Freddie):** legal issuer of record (C-BR-1); primary mint direct to customer wallets (C-BR-2/3); direct redemption + attributed settlement (C-BR-7..10); retail-relationship structure (C-BR-6); Marketing Fee asset/wallet (C-BR-11/12); reward minting (C-BR-13); licensing evidence (C-BR-14); chains + test cap (C-BR-16); immediate wallet registration — accrual not backdated (C-BR-17). C-BR-2/3 and C-BR-7..10 are load-bearing for the v5 architecture.
- **Netbank:** second VA per user (C-NB-1); corporate PHP↔USD conversion + USD funding to Bridge (C-NB-3/4); Disburse-to-Account scope + sandbox (C-NB-5); segregation (C-NB-7).
- **Privy:** user-sole-owner config, no Zed signer, export/recovery, open-loop sends, redemption signing (C-PR-1..5); contract + sandbox.
- **Counsel:** BSP issuer-offer exclusion + FX posture (C-LC-1..4), M-2026-003 (C-LC-5), SEC CASP/exemption/offering/StratBox (C-LC-6..9), security/EMI/disclosures/AMLC (C-LC-10..14) — the R34 launch gates; only items that can block launch after the build is done. Strategy in `regulatory-policy-memo.md`.

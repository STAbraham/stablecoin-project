# Stablecoin project — working conventions

Docs for the Zed Dollar Account (OUSD) pilot. See `ousd-account-prd.md` (PRD, v4) and — once started — `tech-design.md`.

## How iteration works

1. **Drop raw inputs in `inbox/`** — email PDFs, call notes, screenshots, pasted Slack threads, anything. No formatting needed; a `.md` with three bullets from a Netbank call is fine. Name with a date if convenient (`2026-08-18-netbank-call.md`).
2. **Tell Claude "process the inbox"** (any session — the project conventions are in persistent memory). Claude reads each item, updates the PRD / tech design accordingly, appends a changelog entry, moves the item to `inbox/processed/`, and commits.
3. **Review by diff, not by re-reading.** Every doc change is a git commit. Ask Claude "what changed since I last read?" or run `git log --oneline` / `git diff <sha>` — the changelog entries at the top of each doc summarize the same thing in prose.

## Stable anchors (the interface for feedback)

- **Decisions:** D1–D11 in the PRD. To revisit one, reference it by ID ("Netbank says no second VA — reopen D9a").
- **Requirements:** R1–R26, T1–T5 in the PRD.
- **Open questions:** §10, numbered. Partner answers slot in by number ("Freddie answered #1: …").
- The tech design doc will carry the same discipline, plus per-section status tags: `VERIFIED` (checked against code/docs), `ASSUMED` (best guess, safe default), `PENDING <partner>` (blocked on an external answer) — so partner answers map directly to the sections they unblock.

## Current external dependencies (who owes what)

- **Zed → Bridge:** complete KYB (gates OUSD sandbox access).
- **Bridge (Freddie):** rewards mechanics + wallet attribution (§10 #1), OUSD acquire/redeem API + chains, test-cap raise.
- **Netbank:** Disburse-to-Account scope + sandbox credentials; second virtual collection account per user under current agreement.
- **Privy:** contract + sandbox; wallet transaction controls (§10 #5).
- **Counsel:** BSP posture opinion (§10 #8) — only item that can block launch after the build is done.

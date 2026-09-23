# Alternative tracks — exploration hub

**Status:** Live (created 2026-09-14, per Steve). The project now explores **three alternatives in parallel** alongside the incumbent architecture. This file is the comparison board and the rulebook for how parallel exploration works. Read it before touching any `tracks/` doc.

## The four postures

| | **Track 0 — Incumbent** (no new license) | **Track A — OUSD + CASP** | **Track B — OUSD + VASP** | **Track C — USDC + VASP partner + Privy Earn** |
|---|---|---|---|---|
| One-line thesis | Distribute OUSD via primary issuance/redemption, engineered to need no new Zed license (SEC relief sought) | Zed obtains **SEC CASP registration**; no BSP VASP | Zed obtains **BSP VASP license**; no CASP | Zed licenses nothing new: a **licensed PH VASP partner** (e.g., Coins.ph) does the regulated exchange leg; yield comes from **Privy Earn vaults**, not issuer reserve share |
| Stablecoin | OUSD | OUSD | OUSD | USDC |
| Yield source | OS Network Partner Marketing Fee → Zed Rewards | Same as 0 | Same as 0 | DeFi vault yield via Privy Earn (VERIFIED: Aave/Morpho/Kamino/Veda + TMMFs; app share up to 50% of yield) |
| Custody | User-owned Privy, open-loop, no Zed keys | Likely same as 0 (BSP constraints still bind) | Custody becomes *optional* — Zed may hold omnibus | Privy wallets; vault shares self-custodied in user wallet (VERIFIED) |
| Zed economics | Zero spread (R29); Marketing Fee revenue | Marketing Fee; spread posture TBD | **Spread/fees become legal** — licensed exchange economics | Vault fee share VERIFIED (≤50% of yield, Morpho); VASP-partner rev-share PENDING |
| Architecture doc | `../ousd-account-prd.md` (v5.1) + `../regulatory-policy-memo.md` | `a-ousd-casp/track.md` | `b-ousd-vasp/track.md` | `c-usdc-vasp-privy/track.md` |
| Status | **Spec'd** — blocked on C-BR/C-LC confirmations | Exploring | Exploring | **Candidate — PRD v0.1 drafting** (`c-usdc-vasp-privy/prd.md`); Coins.ph partner model confirmed, PH Earn eligibility still open |

## Track lifecycle

`exploring` → `candidate` → `selected` / `parked`

- **exploring** — track.md holds a thesis, a hypothesized architecture (Mermaid sketch), and research questions. Claims are tagged `VERIFIED` / `ASSUMED` / `PENDING <source>` exactly like the tech-design convention.
- **candidate** — research questions substantially closed; track gets a **branded funds-flow diagram** (same HTML→PDF pattern as `../funds-flow-bridge-kyb.html`) and concrete partner asks.
- **selected** — track content merges into the main PRD (new version, changelog entry); other tracks get `parked` with a one-paragraph post-mortem kept in their track.md.
- Tracks are never deleted; a parked track.md records *why*, so re-opening is cheap.

## Workflow rules (extends the README conventions)

1. **Inbox routing.** Drop raw inputs anywhere in `inbox/` — loose is the default and always fine, **including docs that span tracks**; content gets routed at processing time. The `inbox/track-a|b|c/` folders and filename prefixes (`c-…`) are optional hints, nothing more.
2. **Research digestion.** Vendor/partner docs digest where they're used, cited to page/section: track-specific learning → `tracks/<track>/research/<topic>.md`; facts that answer a `../counterparty-counsel-tracker.md` item update **the tracker directly** with the source. The tracker is already the shared layer for cross-track vendor facts, so a multi-track doc needs no special home — e.g., the Privy docs' platform sections close C-PR-1..7 in the tracker (which every track consumes); their Earn sections digest into `c-usdc-vasp-privy/research/privy-earn.md`. The processing report says where each doc's content landed. **The digest, not the raw doc, is what track.md references** — the "grok" artifact.
3. **Track-scoped IDs.** Decisions and questions inside a track use the track prefix: `A-D1`, `B-Q3`, `C-Q7`. Never collide with the main PRD's D/R/T numbering or the tracker's C-* IDs. Cross-reference freely ("same constraint as R30").
4. **Shared counterparty questions** stay in `../counterparty-counsel-tracker.md` (single source of truth for Bridge/Privy/Netbank/counsel confirmations). A track-specific counterparty question lives in the track.md until the track reaches `candidate`, then graduates into the tracker with a C-* ID.
5. **Diagrams.** While `exploring`: Mermaid in track.md (renders on GitHub, cheap to iterate). At `candidate`: branded HTML/PDF funds flow, one per track, `tracks/<track>/funds-flow.html`.
6. **This board stays current.** Any commit that changes a track.md also updates the status row here if the status moved. "What changed?" reviews start here.
7. **Comparison discipline.** When a fact lands that shifts the *relative* attractiveness of tracks (e.g., VASP licensing reopens, Privy Earn unavailable in PH), record it in the **Decision log** below, not just in the affected track.

## Decision log

| Date | Event | Effect on tracks |
|---|---|---|
| 2026-09-14 | Tracks created per Steve; scope expanded to parallel exploration | A/B/C opened at `exploring` |
| 2026-09-23 | Coins.ph integration thread processed (#coins-ph-zed): **direct delivery of USDC to external wallets is native to their order flow** (the Track C custody seam, closed); merchant-hosted KYC pass-through from Persona; per-user VAs on a Zed master account; sequenced settlement; ~2-week integration, test env already live. Track C promoted to candidate; PRD v0.1 started; SOURCES.md bibliography convention added | C advanced to candidate; C-Q9 substantially closed |
| 2026-09-14 | Privy tech docs digested (7 pages from Privy contact). Docs-level custody statements upgrade C-PR-1/2 to working-assumption-docs-supported ("neither Privy nor your application ever sees a user's private key"; "applications cannot transact without explicit user authorization"); Earn deposits are authorization-signed wallet actions (closes most of C-Q4); JWT/OIDC BYO-auth exists (corrects Pete's pre-shared-key-only note; better D7 handoff); dashboard key-quorum approvals map onto R19 dual control for corporate wallets | All tracks + incumbent strengthened; sandbox app creation pending Steve login |
| 2026-09-14 | Privy overview deck (DocSend) + Moreta and Robinhood Earn case studies digested. Robinhood Earn = self-custodial Morpho lending at retail (est. 7% APY, Lloyd's/RELM-insured) — strongest Track C comparable; Moreta = ramp-partner-carries-the-license + Privy + USDC live in SEA incl. PH; Deel's branded DLUSD ("custom stablecoin economics") noted as a second white-label route for the incumbent's scale-up gate; rate benchmarks 3.25%–~7% inform Zed Rewards economics | C strengthened again; white-label note relevant to Track 0's decision gate |
| 2026-09-14 | Privy Earn public docs digested (links via Pete). USDC-on-Base self-serve vaults exist today; vault shares stay self-custodied in user wallets; app fee share up to 50% of yield (Morpho) → Track C's yield + margin mechanisms confirmed. PH eligibility (C-Q6) now the threshold unknown; TMMF variant flagged for counsel (C-Q14) | C strengthened; no change to A/B/0 |

## What would make us pick each (working kill/win criteria — Steve to refine)

- **Track 0 wins** if C-BR-2/3 + C-BR-7..10 confirm and SEC relief (C-LC-6..9) lands on pilot timeline. It's the fastest path and already spec'd.
- **Track A wins** if SEC relief fails/stalls but CASP registration is cheap/fast enough, and BSP posture is unaffected. (A is best understood as *Track 0 + a CASP registration instead of relief* — architecture largely carries over.)
- **Track B wins** if licensed-exchange economics (spread) and product simplicity outweigh licensing cost/timeline — and a VASP license is actually obtainable (moratorium status is the first research question).
- **Track C wins** if Privy Earn yield is competitive and PH-available, the VASP partner takes the exchange/licensing burden cleanly, and DeFi-yield characterization survives counsel review. It's also the only track with no Bridge/OUSD dependency — a genuine hedge against OS/Bridge risk.

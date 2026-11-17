# Netbank QR-PH — API digest (M2 settlement leg)

**Status:** v0.1, 2026-11-17 — digested from Netbank's public Virtual API documentation (virtual.netbank.ph/docs, QR-PH tag; OpenAPI spec embedded in the page). Partner decision per the 11/17 meeting: **Netbank settles M2's PHP leg.** Prior Netbank relationship exists from the incumbent architecture (tracker C-NB items: virtual accounts, Disburse-to-Account, corporate conversion scoping).

## The three QR-PH endpoints

| Endpoint | What it does | Key fields |
|---|---|---|
| `GET /v1/qrph/decode?qr_string=...` | Decodes a scanned QR Ph string into payment details and mints a **`disburse_id`** used to execute payment | Returns: `merchant_name`, `merchant_city`, `merchant_id` (P2M), `amount` (PHP, minor units as string — `50000` = ₱500.00), `destination_account` + `destination_bank_code` (BIC), `qr_transaction_type` (**P2P / P2M**), `qr_type` (**Static / Dynamic**), `reference_number`, `disburse_id` |
| `POST /v1/qrph/transactions` | **Process QRPH disbursement**: debits a **Netbank Corporate Account** and pays the beneficiary per the decoded QR | Request: `disburse_id`, `source_account_number` (Zed's Netbank corporate account), `reference_id` (our idempotency/reference, ≤36 chars), `amount` {cur, num}. Response: `transaction_id`, `status` |
| `POST /v1/qrph/generate` | Generates QR Ph code images (Base64) for *collecting* payments — not needed for M2 spend; relevant someday for receive flows | Ties into their Virtual Collection Account product |

## Transaction lifecycle

`status` enum: **Pending → ForSettlement → Settled**; failure = **Rejected**; plus **NoDisbursement** (empty), and **WaitingForApproval / Approved** — a maker-checker approval regime exists on disbursements (configuration question: per-transaction approval would be fatal for point-of-sale UX; W-Q8). Status lookup: `GET /v1/transactions/{transaction_id}`. The docs carry a webhooks facility (to confirm coverage for QR-PH settlement events vs. polling — W-Q8).

## Facts that shape M2

1. **The disbursement draws on Zed's own prefunded PHP float at Netbank.** Netbank provides payout rails, not conversion. The USDC→PHP leg is entirely outside this API — **the conversion leg is M2's remaining design + counsel question (PRD W-Q7)**: structured wrong (user USDC → Zed, Zed PHP → merchant), Zed performs a crypto-fiat exchange — the VASP-activity perimeter the product posture avoids.
2. **Decode-then-disburse is a clean two-phase fit for the UX:** scan → decode (show merchant + amount + our USDC quote) → user signs → disburse. Static QRs (no amount) need user amount entry; Dynamic QRs carry the amount.
3. **Amounts are PHP minor-unit strings** (two implied decimals) — matches the integer-minor-units ledger convention.
4. **P2P vs P2M is distinguished at decode** — pilot scoping can restrict to P2M (merchants) if desired.
5. `reference_id` (ours, unique) + `transaction_id` (theirs) + decode payload + status trail = the W-R10 traceability chain.

## Open items (→ PRD W-Q8)

Auth scheme (not visible in the public spec extract); webhook coverage for settlement events; settlement timing per destination rail; fees/limits and P2M coverage; corporate-account setup and maker-checker configuration for API-initiated disbursements; sandbox access. Route through the existing Netbank relationship (tracker C-NB contacts).

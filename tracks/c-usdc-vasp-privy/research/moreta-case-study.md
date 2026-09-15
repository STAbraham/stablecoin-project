# Moreta case study (Privy blog) — cross-border stablecoin payments via QR codes

**Source:** blog.privy.io/blog/cross-border-stablecoin-payments-via-qr-codes-with-moreta, captured 2026-09-14 (full-page screenshot in `inbox/processed/privy-blog-moreta-qr-stablecoin-payments.png`).

## What it is
Moreta = travel-payments app: travelers from card-first markets (US/UK/EU) pay QR-code merchants in **Southeast Asia — explicitly "the Philippines, Thailand, and Cambodia, where QR-based wallets are a dominant payment method."** (QR standard not named; in PH that's the QRPH ecosystem.)

## The flow (verbatim-anchored)
1. User funds via "SEPA (for EUR), Faster Payments (for GBP), or by card" — **Coinflow manages the fiat onramp**, crediting Privy embedded wallets 1:1 with USD.
2. "Credits are then redeemed in the background and settled in **USDC**."
3. User pays local QR merchants from the app; Privy provides **smart wallets, gas sponsorship (paymaster/bundler), programmatic transaction initiation**, and funds are "swept to a Moreta-controlled payment wallet."
4. Compliance framing: "**by avoiding direct onramping, Moreta stayed within the bounds of their compliance model**" — the ramp partner carries the licensing burden.

## Why this matters to Zed
1. **It's the Track C thesis, live.** Ramp-partner-carries-the-license + Privy wallets + USDC settlement is exactly the "rent the license" shape — with Coinflow in the role we've penciled for Coins.ph. Coinflow is also worth a look as a comparator for C-Q9 partner-model diligence (what a ramp partner API relationship looks like commercially).
2. **PH QR merchant payments on stablecoin rails exist today** on this stack. Payments are an explicit non-goal for our MVP (§3.1), but this is the roadmap image for "pay from your Dollar Wallet" later — and evidence Privy operates in PH-adjacent products (still does NOT answer C-Q6, whether *Earn* is PH-eligible).
3. **A custody caution, in our favor to know early:** Moreta's pattern uses *programmatic transaction initiation* and sweeps user funds to a **Moreta-controlled wallet** — i.e., the Privy stack happily supports server-initiated, custodial-ish flows. Our no-Zed-signing posture (R31 analog; C-PR-2, C-Q4) is therefore a deliberate configuration we must verify and lock, not a property of the platform.

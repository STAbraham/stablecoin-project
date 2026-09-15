# Privy tech docs (security, auth, wallets, actions, flows, gas, controls) — digest

**Scope note:** cross-track — these facts serve the incumbent (C-PR tracker items, R19 dual control, D7 auth handoff) and all tracks; filed here because Track C prompted the review. Links from Steve's Privy contact, fetched 2026-09-14. Tracker items updated directly where these docs bear on them (per the workflow rule).

## Security architecture (docs.privy.io/security/overview)
- "Privy wallets are **non-custodial** and have a fully **programmable control model**." Keys sharded "across separate security boundaries... never stored in complete form"; operations inside **AWS Nitro Enclave TEEs**.
- Validation: audits by **Cure53, Zellic, Doyensec**; **SOC2 Type I + II**; HackerOne bounty; open-source crypto implementations. → vendor-DD material for counterparty diligence and §8 disclosures.
- Caution retained: the model spans "the full custody spectrum from user-custodial wallets to powerful service-controlled accounts" — our posture is a configuration to lock (consistent with the Moreta caution).

## Non-custodial user wallets (docs.privy.io/wallets/overview/solutions/user-wallets)
The strongest custody statements yet, at docs level:
- "Users retain full custody of their wallets... **Neither Privy nor your application ever sees a user's private key**."
- Keys "only reconstituted in memory inside secure TEEs at the moment a signature is required and **only with the user's explicit authorization**."
- "**Applications cannot transact without explicit user authorization** — signatures require the user's consent before execution."
- Chains: "all EVM chains, all SVM (Solana) chains, Tempo, Bitcoin, Spark, Tron, Stellar, and more."
- **Residual nuance for counsel/Privy:** wallet reconstitution is gated on "a valid user access token from your authentication service" — under bring-your-own-auth, *Zed issues those tokens*. Confirm that token issuance ≠ ability to authorize transactions (i.e., what exactly constitutes "the user's explicit authorization" cryptographically). Logged on C-PR-2.

## Bring-your-own-auth via JWT (docs.privy.io/authentication/user-authentication/jwt-based-auth/overview)
- Privy supports "any OIDC compliant authentication system, including OAuth 2.0, Auth0, Firebase, AWS Cognito, and more": your provider issues the token, "Privy validates this token to authenticate your user."
- **Corrects Pete's 8/24 note** ("only the traditional preshared key flow"): that applied to the *custom OAuth* method; JWT-based stateless auth is a separate, supported path — and the natural fit for D7's session handoff (Zed's existing auth issues the token; no separate Privy login).

## Wallet actions (docs.privy.io/wallets/actions/overview)
- Actions: **transfer, swap, earn, payout/fiat** — note a *fiat payout* exists as a wallet action (Privy-side analog to parts of our Netbank/Bridge legs; not actionable now, relevant to long-run vendor questions).
- **Authorization model:** "For wallets with an owner and/or signers, requests to wallet actions APIs require an **authorization signature over the request**," verified in the TEE. For user-owned wallets that signer is the user → **this substantially answers C-Q4's open item** (Earn deposits/withdrawals are authorization-signed wallet actions, not naked server calls).
- Per-action policy methods exist; caveat: "Privy does not enforce policy rules for RPC methods that may internally be used implicitly by the wallet action" — read carefully when designing C-PR-6 controls.

## Financial flows (docs.privy.io/financial-flows/overview)
- Six services: wallets, deposits ("crypto and fiat sources"), payouts ("crypto and fiat"), **Earn**, cards, trade — "without... taking custody of funds."
- Fiat rails/partners/countries not enumerated in the overview → the PH-availability question (C-Q6) stays a Privy-conversation item.

## Gas (docs.privy.io/wallets/gas-and-asset-management/gas/overview)
- **App pays:** gas credits; EVM via "EIP-7702 with paymasters" (Base included); Solana via Privy-managed fee payer; billed as "actual network gas cost plus a convenience fee."
- **User pays:** EVM only, from the wallet's **USDC/USDT/EURC/USDG** balance — users never need native tokens either way. Good for Track C UX (deposits/withdrawals gasless from the user's perspective).

## Treasury workspace / controls (docs.privy.io/controls/dashboard/overview)
- **Manual approvals with key quorums:** propose intent (API or dashboard) → review queue → quorum members "approve or reject... via the Privy Dashboard," secured by "biometric or TOTP MFA." Quorum can be **owner** (full control) or **signer** (approve transactions only).
- **Direct mapping to R19 (dual control):** Zed's corporate on-chain wallets (Marketing Fee payout wallet in the incumbent; Earn admin/fee wallet in Track C) can enforce initiate-vs-approve separation inside Privy's own governance rather than only via Slack process. Flag for tech design.
- (The Privy contact's blurb describes a "Treasury workspace" for managing stablecoin earnings/balance sheet with governance controls; the docs page covers the governance half. Balance-sheet views: verify in the sandbox.)

## Access report
All seven docs URLs publicly accessible 9/14. `dashboard.privy.io` requires login (expected) — sandbox exploration + app creation pending Steve's session.

# Privy overview deck (14 slides, via DocSend) — digest

**Source:** DocSend `d3qrnv8en3g8dfh3`, captured 2026-09-14 → screenshots in `inbox/processed/docsend-d3qrnv8en3g8dfh3/`. Privy sales/overview deck ("Privy, a Stripe company"), marked Confidential. Marketing-level claims — treat as *evidence*, not configuration-level confirmation.

## Platform facts (cross-track; annotated onto tracker items as evidence)
- **Scale/credibility (slide 2):** 2,000+ teams, 160M+ accounts, 180+ countries, $18B+ monthly transaction volume. Customers: Stripe, Ramp, Deel, Robinhood, Klarna, Jeeves, Gusto, ADP, Remitly, Félix, Slash, Onafriq, Kraken, Uniswap, Hyperliquid, Fomo.
- **Custody (slide 12):** "Flexible custody — support both non-custodial and custodial wallet models, depending on your product and regulatory requirements." → supportive of C-PR-1 (user-owned config exists) but *also* proves the custodial path exists — our posture is a **configuration choice that must be verified and locked** (C-PR-1/2).
- **Policies (slide 12):** "Programmable policies and controls — define what actions can be taken, by whom, and under what conditions with granular authorization policies." → supportive of C-PR-6 (controls without custody), same caveat.
- **Compliance (slide 12):** KYC/KYB + transaction screening integrable with "supported compliance providers." **Key management:** TEEs, can incorporate own key material.
- **One-API breadth (slides 5/11):** hold (wallets) / move (fund via bank, cards, crypto; global payouts; card issuing) / grow (yield, tokenized MMFs, RWAs, onchain markets); 40+ chains; "bring your own authentication" (matches the custom-OAuth page Pete sent).
- **Partnership model (slide 13):** Discovery → Design ("align on architecture, security, compliance, and legal considerations before you build") → Implementation with embedded FDEs → Launch → Scale. Useful: Privy expects to co-design around regulatory needs — bring the tracker's C-PR items to that Design phase.

## Yield comparables (Track C economics context — C-Q3/C-Q13)
- **Ramp (slide 7):** businesses "hold dollar-backed stablecoins directly in Ramp and earn **up to 3.25% in rewards**"; pay USDC/USDT to 140+ countries, fiat in 40+ currencies via local rails.
- **Robinhood (slide 10):** "lend dollar-backed **USDG** from a non-custodial wallet and earn an estimated **7% APY**" in-app. Non-custodial lending yield at retail scale = the Track C shape, live at Robinhood.
- **Deel (slide 9):** dollar balances in 80+ countries + "**Earn vault**" on idle balances + "**Custom stablecoin economics** — issue a branded stablecoin (DLUSD) and participate in the economics of balances held across the Deel ecosystem."
- **Félix (slide 8):** US→LatAm remittances over WhatsApp on stablecoin rails (corridor/UX comparable).

## Implications for Zed
1. **Rate benchmark:** user-facing rewards in the wild: 3.25% (Ramp, business) to ~7% est. (Robinhood, DeFi lending). Zed Rewards under the OUSD Marketing-Fee model (~3.75% gross illustrative) sits at the low end; Track C vault yield could support Robinhood-like rates. Feeds Open Question #1 / C-INT-3 economics.
2. **Deel's DLUSD precedent** — "issue a branded stablecoin and participate in the economics" through the Privy/Stripe stack — is directly relevant to the **white-label scale-up gate** in the incumbent PRD (§9 decision gate): a second issuance route to price against Bridge's minimum-mint model when that decision comes.
3. Privy's breadth (cards, payouts, ramps) means several things Zed sources elsewhere (Netbank disbursement, Bridge rails) have Privy-stack analogs — not actionable now, but relevant to long-run vendor consolidation questions.

# ASTRA Trader v1

ASTRA Trader is a safety-first extension layer built on top of this OpenAlgo fork.

## Current mode

Paper trading only. Live order execution is intentionally not implemented in this layer.

## Design

Market/portfolio data -> signal scoring -> deterministic risk checks -> paper execution -> journal/analytics.

The risk engine, not an LLM, controls whether a trade is allowed and how large it may be.

## Default guardrails

- 0.5% equity risk per trade
- 2% maximum daily loss
- maximum 3 losing trades per day
- 1.5% maximum aggregate open risk
- minimum score 78/100
- maximum spread 1.5%
- maximum position notional 20% of equity
- master kill switch support

## Security rules

- Never commit broker credentials, INDmoney credentials, OTPs, MPINs, access tokens, cookies, environment files, database dumps, or private keys.
- Keep INDmoney integration read-only.
- Keep broker execution adapters disabled until explicitly reviewed.
- Use broker-side permissions, IP allowlisting and order/risk limits when live execution is eventually introduced.

## Next modules

1. INDmoney read-only data adapter
2. NIFTY/BANKNIFTY/F&O scanner
3. options-chain normalization
4. trade journal and P&L reconciliation
5. backtest harness
6. alerting/dashboard
7. optional broker execution adapter behind an explicit feature flag

# ASTRA Broker / Data Integration Selection

## Primary user account context: INDmoney

INDmoney is the preferred portfolio + market-context source for ASTRA.

Official INDmoney MCP is first-party and read-only by design. It can expose portfolio holdings, live Indian stock/F&O positions, watchlists, option-chain/Greeks/history and market data, subject to the user's approved scopes.

INDmoney MCP cannot place trades, transfer money, redeem investments or change account settings.

## Architecture decision

- INDmoney = read-only portfolio, positions and market-context layer.
- ASTRA research/risk/paper/shadow logic may consume INDmoney data after an official connection is available.
- Real order transmission must remain a separate broker-execution adapter using an official supported trading API.
- No scraping, browser automation or unofficial INDmoney execution path is permitted.

## Current live-execution status

No execution broker is selected yet.

LIVE remains disabled.

Before any real execution adapter can be considered:
1. official broker API selected,
2. account/API credentials connected securely,
3. static-IP/compliance requirements satisfied,
4. startup reconciliation proven,
5. idempotency and unknown-submission recovery proven,
6. kill switch tested,
7. LIMITED_LIVE validation completed,
8. explicit user authorization obtained.

This document is architecture selection only, not authorization to trade.

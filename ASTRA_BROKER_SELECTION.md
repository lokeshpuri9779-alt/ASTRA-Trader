# ASTRA Broker Selection

Selected target: Upstox Developer API

## Why Upstox

- Official retail trading API.
- API and market-data access advertised at ₹0.
- Explicit 2026 static-IP management support, including primary/secondary IPs.
- Official algo-trading compliance documentation effective 1 April 2026.
- Read-only Analytics Token with long-lived access for portfolio/market-data workflows.
- Positions, holdings, funds, historical data and market-data APIs are available separately from order placement.
- Order placement can remain isolated behind ASTRA's execution adapter and live gate.

## Current integration policy

ASTRA will treat Upstox as the broker adapter target, but LIVE transmission remains disabled.

Required before any real order can be considered:
1. Upstox account connection.
2. App/API credentials.
3. Primary static IP registration; secondary IP recommended.
4. Daily authentication/session lifecycle.
5. Startup reconciliation against broker positions/orders.
6. Broker-specific idempotency/unknown-submission handling.
7. Kill-switch verification.
8. LIMITED_LIVE validation.
9. Explicit user authorization for real-money activation.

## Alternatives considered

- Zerodha Kite Connect: mature and robust, but full realtime/historical Connect tier is paid.
- FYERS: free trading API and compliant static-IP flow, but Upstox currently offers clearer programmatic static-IP management plus read-only analytics-token support.
- DhanHQ: free trading API; data API is paid separately.

This document is architecture selection only, not authorization to trade.

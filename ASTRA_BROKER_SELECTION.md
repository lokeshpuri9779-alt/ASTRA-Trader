# ASTRA Broker / Data Integration Selection

## Data and portfolio context: INDmoney

INDmoney remains ASTRA's preferred read-only source for:
- portfolio holdings,
- live Indian stock/F&O positions,
- market context,
- option-chain/Greeks/history.

INDmoney is not used for real-money order execution.

## Execution target: Upstox Developer API

Selected as ASTRA's execution-broker target because the current official platform provides:
- official retail order APIs,
- trading/data API usage without a separate API fee,
- explicit primary/secondary static-IP management for the 2026 retail-algo framework,
- a first-party sandbox environment for end-to-end order-flow testing before live execution,
- portfolio/funds/order APIs required for reconciliation and monitoring.

## Architecture

INDmoney -> read-only portfolio/market intelligence
ASTRA -> research, risk, paper, shadow, reconciliation and promotion gates
Upstox Sandbox -> broker integration and execution-flow validation
Upstox Live -> disabled until all external and safety gates are complete

## Hard gates before any live order

1. User connects an Upstox account and developer app.
2. Static IP is provisioned and registered.
3. Sandbox adapter passes order lifecycle tests.
4. Startup position/order reconciliation passes.
5. Broker-specific idempotency and unknown-submission recovery are proven.
6. Kill switch is proven against broker-specific behavior.
7. LIMITED_LIVE validation is completed.
8. Explicit user authorization for real-money activation is obtained.

This document selects an integration target only. It does not authorize live trading.

# ASTRA Trader v1 Code Architecture

The v1 codebase now separates concerns explicitly:

- core/ — canonical event model and execution modes
- data/ — market-data source interfaces and normalization boundary
- strategies/ — strategy interfaces only; no broker calls
- risk.py — deterministic trade-level risk
- portfolio/ — portfolio state and later allocation/risk aggregation
- execution/ — order intents and gateway abstractions
- paper.py — simulated execution only
- observability/ — health states and operational monitoring
- app.py — application composition root

## Safety default

ASTRA Trader v1 defaults to PAPER.

Live broker execution is not wired into the application shell.

## Architectural rules

1. Strategies emit trade signals, never broker API calls.
2. Risk converts/blocks signals before order creation.
3. Execution gateways receive already-approved order intents.
4. Every live-capable order must have a durable client_order_id.
5. Market data, strategy, risk, portfolio and execution remain independently testable.
6. Broker-specific code must stay behind execution adapters.
7. AI/ML components cannot call execution directly.
8. Health/risk state may block execution at any point.
9. The same strategy/event interfaces should be reusable for replay, paper, shadow and live.
10. LIVE remains an explicit future capability, not a default mode.

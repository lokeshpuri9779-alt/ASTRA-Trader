# ASTRA Trader Implementation Queue

This is the ordered build queue. Work through it continuously without requiring user confirmation between milestones unless an external credential, account action, or irreversible live-trading decision is required.

## Phase 1 — Replay & execution realism
- [x] deterministic event replay
- [x] bid/ask market fills
- [x] partial-fill / volume-cap model
- [x] slippage hooks
- [x] stop gap-through behavior
- [x] date-versioned cost hooks
- [x] limit-order fill logic
- [x] complete order state machine
- [x] simulated broker rejections
- [x] latency scheduler
- [x] margin/accounting ledger
- [x] portfolio P&L reconciliation
- [x] expiry/settlement processor
- [x] scenario stress engine

## Phase 2 — Data
- [x] normalized Instrument / Bar / Quote
- [x] versioned instrument master
- [x] NSE UDiFF parser
- [x] index/VIX loader
- [x] option observation schema
- [x] ingestion SHA-256 manifests
- [x] Parquet adapter
- [x] raw ZIP/archive ingestion
- [x] persistent instrument-master import/export
- [x] option-chain snapshot parser
- [x] NIFTY / BANKNIFTY / India VIX source fixtures
- [x] point-in-time dataset manifest builder
- [x] data-quality quarantine pipeline

## Phase 3 — Research engine
- [x] experiment manifest
- [x] append-only experiment ledger
- [x] hypothesis schema
- [x] experiment runner
- [x] parameter sweep runner
- [x] chronological train/validation/test splitter
- [x] walk-forward runner
- [x] purging + embargo
- [x] CPCV support
- [x] Monte Carlo trade-sequence tests
- [x] placebo / permutation tests
- [x] parameter-surface robustness
- [x] Deflated Sharpe / multiple-testing diagnostics
- [x] candidate dossier generator

## Phase 4 — Strategy & regime library
- [x] trend / breakout baseline
- [x] relative-strength momentum baseline
- [x] VWAP / z-score mean-reversion baseline
- [x] volatility-expansion baseline
- [x] IV-vs-realized-volatility features
- [x] OI / PCR contextual features
- [x] skew / term-structure features
- [x] rule-based regime engine
- [x] expiry-regime engine
- [x] HMM/clustering challenger only after baseline

## Phase 5 — Portfolio/risk
- [x] deterministic trade-level risk engine
- [x] portfolio exposure aggregator
- [x] sector / underlying / correlation caps
- [x] volatility-adjusted sizing
- [x] drawdown throttle
- [x] options Greek aggregation
- [x] scenario/CVaR stress limits
- [x] liquidity-aware position caps
- [x] simultaneous-signal allocator
- [x] strategy risk budgets

## Phase 6 — Paper & shadow
- [x] basic paper broker
- [x] full simulated order book
- [x] persistent paper portfolio
- [x] shadow-order gateway
- [x] replay vs paper vs shadow divergence metrics
- [x] daily journal and performance attribution
- [x] dashboard/alerts
- [x] INDmoney-driven shadow runtime
- [x] shadow-run journal with explicit no-execution marker

## Phase 7 — INDmoney read-only
- [x] official INDmoney connector connected and verified read-only
- [x] immutable account snapshot model
- [x] adapter interface
- [x] portfolio/positions ingestion boundary
- [x] read-only market/context ingestion where officially available
- [x] normalization into ASTRA portfolio schema
- [x] security/redaction tests

## Phase 8 — Observability & self-healing
- [x] health-state model
- [x] subsystem heartbeats
- [x] stale-data monitor
- [x] broker/data reconciliation monitor
- [x] strategy degradation monitor
- [x] drift monitor
- [x] incident ledger
- [x] watchdog
- [x] safe auto-disable / recovery rules
- [x] daily health report

## Phase 9 — Security & deployment
- [x] secret-scan CI (manual-only; automatic CI disabled by user)
- [x] dependency-scan CI (manual-only; automatic CI disabled by user)
- [x] test CI for ASTRA modules (manual-only; automatic CI disabled by user)
- [x] environment separation: research/paper/shadow/live
- [x] immutable release/version stamping
- [x] audit-log persistence
- [x] backup/restore tests
- [x] live feature flag defaults OFF

## Phase 10 — Live broker execution
DO NOT implement or enable until Phases 1–9 pass validation.
- [x] execution broker adapter selected — Upstox Developer API; INDmoney remains read-only data/context source
- [x] current India retail-algo compliance re-verified
- [ ] static-IP/deployment requirements satisfied (external account/infrastructure step)
- [ ] idempotent order submission (blocked pending approved broker-specific live integration)
- [x] startup reconciliation (broker-agnostic primitive)
- [x] unknown-submission recovery policy
- [x] broker kill switch primitive
- [x] LIMITED_LIVE guardrails (no broker transmission)
- [x] production promotion gates
- [x] Upstox sandbox execution contract (no live transmission)

## Rule

Continue automatically through this queue. Automatic GitHub CI triggers are disabled by user request; do not re-enable unless explicitly asked.
Stop and ask the user only when:
1. external credentials/account connection are required,
2. the user must perform an irreversible external action,
3. enabling real-money LIVE trading is being considered,
4. a material safety/compliance blocker appears.

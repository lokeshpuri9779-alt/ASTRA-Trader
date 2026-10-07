# ASTRA Trader Implementation Queue

This is the ordered build queue. Work through it continuously without requiring user confirmation between milestones unless an external credential, account action, or irreversible live-trading decision is required.

## Phase 1 — Replay & execution realism
- [x] deterministic event replay
- [x] bid/ask market fills
- [x] partial-fill / volume-cap model
- [x] slippage hooks
- [x] stop gap-through behavior
- [x] date-versioned cost hooks
- [ ] limit-order fill logic
- [ ] complete order state machine
- [ ] simulated broker rejections
- [ ] latency scheduler
- [ ] margin/accounting ledger
- [ ] portfolio P&L reconciliation
- [ ] expiry/settlement processor
- [ ] scenario stress engine

## Phase 2 — Data
- [x] normalized Instrument / Bar / Quote
- [x] versioned instrument master
- [x] NSE UDiFF parser
- [x] index/VIX loader
- [x] option observation schema
- [x] ingestion SHA-256 manifests
- [x] Parquet adapter
- [ ] raw ZIP/archive ingestion
- [ ] persistent instrument-master import/export
- [ ] option-chain snapshot parser
- [ ] NIFTY / BANKNIFTY / India VIX source fixtures
- [ ] point-in-time dataset manifest builder
- [ ] data-quality quarantine pipeline

## Phase 3 — Research engine
- [x] experiment manifest
- [x] append-only experiment ledger
- [ ] hypothesis schema
- [ ] experiment runner
- [ ] parameter sweep runner
- [ ] chronological train/validation/test splitter
- [ ] walk-forward runner
- [ ] purging + embargo
- [ ] CPCV support
- [ ] Monte Carlo trade-sequence tests
- [ ] placebo / permutation tests
- [ ] parameter-surface robustness
- [ ] Deflated Sharpe / multiple-testing diagnostics
- [ ] candidate dossier generator

## Phase 4 — Strategy & regime library
- [ ] trend / breakout baseline
- [ ] relative-strength momentum baseline
- [ ] VWAP / z-score mean-reversion baseline
- [ ] volatility-expansion baseline
- [ ] IV-vs-realized-volatility features
- [ ] OI / PCR contextual features
- [ ] skew / term-structure features
- [ ] rule-based regime engine
- [ ] expiry-regime engine
- [ ] HMM/clustering challenger only after baseline

## Phase 5 — Portfolio/risk
- [x] deterministic trade-level risk engine
- [ ] portfolio exposure aggregator
- [ ] sector / underlying / correlation caps
- [ ] volatility-adjusted sizing
- [ ] drawdown throttle
- [ ] options Greek aggregation
- [ ] scenario/CVaR stress limits
- [ ] liquidity-aware position caps
- [ ] simultaneous-signal allocator
- [ ] strategy risk budgets

## Phase 6 — Paper & shadow
- [x] basic paper broker
- [ ] full simulated order book
- [ ] persistent paper portfolio
- [ ] shadow-order gateway
- [ ] replay vs paper vs shadow divergence metrics
- [ ] daily journal and performance attribution
- [ ] dashboard/alerts

## Phase 7 — INDmoney read-only
- [ ] adapter interface
- [ ] portfolio/positions ingestion
- [ ] read-only market/context ingestion where officially available
- [ ] normalization into ASTRA portfolio schema
- [ ] security/redaction tests

## Phase 8 — Observability & self-healing
- [x] health-state model
- [ ] subsystem heartbeats
- [ ] stale-data monitor
- [ ] broker/data reconciliation monitor
- [ ] strategy degradation monitor
- [ ] drift monitor
- [ ] incident ledger
- [ ] watchdog
- [ ] safe auto-disable / recovery rules
- [ ] daily health report

## Phase 9 — Security & deployment
- [ ] secret-scan CI
- [ ] dependency-scan CI
- [ ] test CI for ASTRA modules
- [ ] environment separation: research/paper/shadow/live
- [ ] immutable release/version stamping
- [ ] audit-log persistence
- [ ] backup/restore tests
- [ ] live feature flag defaults OFF

## Phase 10 — Live broker execution
DO NOT implement or enable until Phases 1–9 pass validation.
- [ ] broker adapter selected
- [ ] current India retail-algo compliance re-verified
- [ ] static-IP/deployment requirements satisfied
- [ ] idempotent order submission
- [ ] startup reconciliation
- [ ] unknown-submission recovery
- [ ] broker kill switch
- [ ] LIMITED_LIVE mode
- [ ] production promotion gates

## Rule

Continue automatically through this queue.
Stop and ask the user only when:
1. external credentials/account connection are required,
2. the user must perform an irreversible external action,
3. enabling real-money LIVE trading is being considered,
4. a material safety/compliance blocker appears.

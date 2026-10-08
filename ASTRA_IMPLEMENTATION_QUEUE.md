# ASTRA Trader Optimized Implementation Queue

Work continuously through safe items without requiring user confirmation. Automatic CI remains disabled by user request.

## DONE — Core system
Phases 1–9 are complete and validated:
- replay/execution realism
- data pipeline
- research engine
- strategy/regime library
- portfolio/risk
- paper/shadow trading
- INDmoney read-only integration
- observability/self-healing
- security/deployment foundations

## PHASE 10A — Internal safe broker-readiness work
Complete these before asking the user for any external setup.

- [x] execution target selected: Upstox Developer API
- [x] INDmoney retained as read-only portfolio/market-context source
- [x] India retail-algo compliance re-verified
- [x] generic startup reconciliation primitive
- [x] unknown-submission recovery policy
- [x] generic kill-switch primitive
- [x] LIMITED_LIVE guardrails
- [x] production promotion gates
- [x] Upstox sandbox execution contract
- [x] deterministic Upstox sandbox simulator
- [x] Upstox order-state lifecycle mapper
- [x] Upstox reconciliation mapper
- [x] Upstox static-IP configuration validator
- [x] sandbox idempotency key policy
- [x] sandbox duplicate-order protection
- [x] sandbox unknown-submission recovery test
- [x] sandbox kill-switch test
- [x] sandbox reconciliation test
- [x] consolidated broker-readiness report
- [x] secure Upstox credential readiness checker
- [x] Upstox connection readiness evaluator
- [x] Upstox external setup runbook

## PHASE 11 — Unattended paper execution (priority)
- [x] one-shot offline paper runner (no network/broker)
- [x] signal -> risk -> executable bid/ask -> simulated fill -> JSONL journal
- [x] fail-closed stale data/missing quotes/price mismatch
- [x] batch buying-power and risk reservation
- [x] CLI and regression test definitions (execution not yet verified)
- [ ] run tests in a Python environment; resolve discovered failures (local GitHub clone blocked by DNS)
- [ ] select an authorized market data source accessible to persistent runtime
- [ ] authenticated read-only collector; no secrets in GitHub
- [ ] real strategy signals from actual time-series inputs (never fabricated)
- [x] persistent cycle-ID claim and duplicate-run suppression (local filesystem)
- [ ] durable positions/cash/P&L across cycles, including restart reconciliation
- [x] paper-only scheduler entry point requiring an explicit PAPER manifest
- [ ] deploy paper-only scheduler and verify consecutive unattended runs
- [ ] independent trading logs confirming actual SIMULATED_FILL or legitimate WAIT/REJECT outcomes

## PHASE 10B — External setup blocker
Only stop when Phase 10A is complete. All preparatory code is complete; this phase now requires the user's real Upstox account/infrastructure.

- [ ] user connects Upstox developer account/app
- [ ] API credentials connected securely
- [ ] primary static IP provisioned
- [ ] secondary static IP provisioned or explicitly waived
- [ ] static IP registered with broker
- [ ] broker authentication/session flow verified
- [ ] read-only broker positions/orders/funds snapshot verified

## PHASE 10C — Pre-live validation
No live-money execution yet.

- [ ] run real Upstox sandbox lifecycle end-to-end
- [ ] run startup reconciliation against connected broker
- [ ] prove broker-specific idempotency
- [ ] prove unknown-submission recovery
- [ ] prove broker-specific kill switch
- [ ] complete shadow vs broker-sandbox divergence checks
- [ ] complete LIMITED_LIVE dry-run readiness review
- [ ] zero unresolved safety incidents

## PHASE 10D — Real-money activation
Requires explicit user authorization.

- [ ] user explicitly authorizes LIMITED_LIVE
- [ ] activate minimal-capital LIMITED_LIVE mode
- [ ] monitor/reconcile every order
- [ ] halt automatically on any mismatch
- [ ] promote only after LIMITED_LIVE evidence passes production gates

## Rule
Continue automatically through Phase 10A.
Stop only for:
1. external credentials/account connection,
2. static-IP/account actions,
3. irreversible external actions,
4. explicit real-money authorization,
5. material safety/compliance blocker.

Do not re-enable automatic CI unless explicitly requested.

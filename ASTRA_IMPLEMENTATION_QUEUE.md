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

## PHASE 10B — External setup blocker
Only stop when Phase 10A is complete.

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

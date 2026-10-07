# ASTRA Production Observability & Self-Healing

Status: research/design only. No live auto-recovery enabled.

## Objective

ASTRA should detect faults early, reduce risk automatically, and recover only when recovery is provably safe.

The system should prefer:
HEALTHY -> DEGRADED -> SAFE/HALTED
rather than
HEALTHY -> UNKNOWN -> keep trading.

## Health domains

Monitor separately:

### Market data
- feed connected
- event freshness
- missing symbols
- timestamp monotonicity
- duplicate bursts
- crossed/invalid quotes
- abnormal price gaps
- option-chain completeness

### Broker/execution
- authentication valid
- API latency
- acknowledgement latency
- rejection rate
- order-state divergence
- position reconciliation
- funds/margin freshness
- reconnect count
- rate-limit usage

### Strategy
- signal generation alive
- expected cadence
- rolling expectancy
- drawdown
- hit rate
- turnover
- slippage
- regime attribution
- prediction/calibration drift for ML strategies

### Portfolio/risk
- total open risk
- leverage
- delta/gamma/vega exposure
- concentration
- daily loss
- rolling drawdown
- margin buffer
- liquidity risk

### Infrastructure
- process uptime
- CPU/memory/disk
- database health
- clock synchronization
- queue lag
- log ingestion
- dependency/service availability

## Health state model

Each subsystem reports one of:

HEALTHY
DEGRADED
UNSAFE
UNKNOWN

Portfolio-level state is derived conservatively.

Examples:
- stale market data -> DEGRADED/UNSAFE depending on age
- unresolved broker mismatch -> UNSAFE
- missing monitoring data -> UNKNOWN, treated conservatively
- strategy underperformance -> DEGRADED, not necessarily infrastructure failure

## Safe degradation

When degraded, ASTRA should reduce capabilities rather than attempt full operation.

Examples:
- stale option-chain feed:
  disable option entries dependent on chain features
- broker reconciliation warning:
  block new exposure, allow safe reconciliation/cancels
- ML model unavailable:
  disable strategies requiring that model
- secondary analytics DB down:
  continue only if execution/risk state remains authoritative and auditable

Never substitute fabricated/default market inputs.

## Failure hierarchy

### Level 0 — informational
No action beyond logging.

### Level 1 — warning
Continue with monitoring.

### Level 2 — degraded
Reduce risk or disable affected strategy/feature.

### Level 3 — block new risk
No new exposure until resolved.

### Level 4 — emergency
Global kill switch / explicit risk-reduction procedure.

Severity should be deterministic and documented.

## Auto-disable rules

Examples:
- market-data age beyond threshold
- repeated order rejection spike
- reconciliation mismatch
- realized slippage far beyond validated range
- strategy drawdown breach
- rolling expectancy materially below lower confidence bound
- feature/model drift beyond threshold
- corrupted instrument master
- margin buffer below minimum
- exchange/broker connectivity unstable

Auto-disable should normally stop NEW risk first.

## Self-healing policy

Allowed automatic recovery:
- reconnect idempotent market-data stream
- restart stateless worker
- reopen read-only data connection
- refresh cached instrument metadata from trusted source
- retry safe/idempotent GET requests
- fail over to approved redundant data source
- rebuild derived features from canonical raw events

Restricted recovery:
- order resubmission
- position flattening
- credential rotation
- live mode re-enable
- strategy promotion

These require stricter deterministic checks and, where appropriate, manual approval.

## Recovery state machine

FAULT_DETECTED
-> ISOLATED
-> SAFE_STATE
-> DIAGNOSIS
-> RECOVERY_ATTEMPT
-> REVALIDATION
-> RESTORED

or

-> HALTED

RESTORED requires all mandatory health checks to pass.

Do not automatically jump from reconnect success to live trading.

## Revalidation after recovery

Before re-enabling affected execution:
- data fresh
- clock sane
- broker authenticated
- orders reconciled
- positions reconciled
- funds/margin refreshed
- risk limits recomputed
- kill switches checked
- affected strategy state rebuilt
- no duplicate intent pending

Then resume at the lowest safe capability.

## Broker outage behavior

If broker API becomes unavailable:
- freeze new entries
- retain local state
- preserve all intents/events
- keep monitoring market data if available
- retry only safe status/read operations
- on reconnect, reconcile before any new order

If exits cannot be submitted, raise highest-priority alert and do not pretend risk is controlled.

## Market data outage behavior

If primary feed fails:
- mark all dependent prices stale
- stop new entries using stale instruments
- optionally fail over only to an approved equivalent source
- tag source switch in audit log
- require continuity/quality checks

Do not stitch incompatible feeds silently.

## Database failure behavior

Use authoritative separation:
- append-only execution journal / durable order state is critical
- analytics storage is secondary

If durable execution state cannot be written:
BLOCK_NEW_ORDERS

Trading without durable state is unacceptable.

## Clock integrity

Trading systems depend on time.

Monitor:
- NTP/system clock drift
- timezone
- exchange calendar
- DST for non-India markets

If clock drift exceeds threshold:
block latency-sensitive/new execution until corrected.

## Strategy degradation monitoring

A live strategy should be evaluated against expected distributions, not one loss.

Track rolling:
- expectancy
- variance
- drawdown
- win/loss size
- trade frequency
- exposure
- slippage
- regime mix

Compare to validation confidence bands.

Possible states:
NORMAL
WATCH
THROTTLED
DISABLED

## Model drift

For ML strategies monitor:
- feature drift
- prediction drift
- calibration drift
- residual drift
- regime-frequency drift

If drift exceeds policy:
- reduce model weight
- switch to baseline strategy if validated
- or disable model-dependent entries

Do not retrain automatically during live session.

## Slippage / execution drift

Compare:
expected fill
vs
actual fill.

Track by:
- instrument
- time of day
- volatility regime
- order type
- quantity/liquidity bucket
- expiry distance

Large persistent deterioration can invalidate a strategy even when its raw signals remain correct.

## Alerts

Alert content should include:
- severity
- subsystem
- exact failure
- current exposure
- automatic action taken
- whether new orders are blocked
- required human action, if any
- event ID

Avoid alert spam by:
- deduplication
- cooldowns
- aggregation
- escalation on persistence/severity

## Daily health report

Generate a concise daily report:
- uptime
- data gaps
- broker errors
- reconciliation mismatches
- order rejects
- slippage
- strategy P&L and drawdown
- risk-limit events
- auto-disable events
- unresolved incidents

## Incident ledger

Each incident records:
- incident_id
- start/end
- severity
- affected components
- market exposure during event
- root cause
- automatic actions
- manual actions
- financial impact
- remediation
- recurrence-prevention task

Incidents remain searchable.

## Chaos / failure testing

Before live, simulate:
- market-data disconnect
- broker timeout
- partial broker response
- database unavailable
- duplicate message
- process crash
- network partition
- token expiry
- stale clock
- malformed quote
- extreme volatility
- rate-limit exhaustion

Pass condition:
system reduces/contains risk and recovers deterministically.

## Redundancy

Redundancy can improve resilience but can also introduce inconsistent state.

Use redundant:
- monitoring
- read-only market data where validated
- backups
- stateless services

Be cautious with active-active order execution.

There should be one authoritative execution coordinator per account/strategy scope unless a formally tested consensus/idempotency design exists.

## Watchdog

A watchdog may:
- check heartbeats
- detect stale workers
- restart stateless services
- set kill switch
- page/alert

It must not:
- invent missing state
- submit replacement orders blindly
- reactivate live trading without reconciliation

## Backups

Back up:
- configuration
- audit logs
- experiment manifests
- model artifacts
- strategy versions
- execution journal

Never back up plaintext secrets into ordinary repo/storage.

Test restoration periodically.

## Observability stack

Conceptual components:
- structured logs
- metrics/time-series
- traces for critical order paths
- health endpoints
- dashboards
- alert routing
- incident ledger

Every order should be traceable from:
market event -> signal -> risk decision -> order intent -> broker response -> fill -> portfolio update.

## Initial ASTRA self-healing policy

Automatic:
- restart stateless data/research workers
- reconnect read-only feeds
- retry idempotent reads
- quarantine bad data
- disable affected strategy
- block new risk
- activate kill switch

Not automatic initially:
- re-enable live after major fault
- flatten all positions
- resubmit ambiguous orders
- rotate credentials
- modify strategy parameters

## Core principle

Self-healing means restoring verified safe operation.

It does not mean aggressively forcing the system back online.

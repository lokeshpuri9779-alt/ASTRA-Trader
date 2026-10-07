# ASTRA Live Execution Reliability & Security

Status: research/design only. No live trading enablement.

## Objective

Live execution must fail safely.

ASTRA must assume:
- networks fail
- brokers time out
- acknowledgements arrive late
- duplicate requests occur
- processes restart
- data becomes stale
- credentials can be targeted
- exchange/broker rules change

The system should convert those failures into halted or reconciled states rather than uncontrolled orders.

## Compliance boundary

For India retail algo trading, execution design must follow the current broker/exchange framework.

Current implementation references indicate:
- API-originating retail algo orders are subject to the retail algo framework from 1 April 2026.
- Transactional API execution requires broker-approved/static-IP infrastructure according to current implementation standards.
- Daily broker login/token lifecycle must be respected.
- Higher-order-rate strategies may require registration/other broker-exchange handling.

ASTRA must not try to bypass broker, exchange, static-IP, tagging, registration or authentication requirements.

## Four execution environments

RESEARCH
- no broker connection

PAPER
- live/recorded market data
- simulated orders only

SHADOW
- creates the exact intended orders
- does not submit them
- records what would have happened

LIVE
- broker order submission enabled only behind explicit configuration and risk gates

Mode must be visible and immutable during an order lifecycle.

## Idempotent order intent

Every logical order gets a unique client_order_id generated before broker submission.

Persist before network call:
- client_order_id
- strategy/version
- signal id
- instrument
- side
- quantity
- order type
- limit/trigger
- portfolio/risk snapshot
- creation timestamp
- intent hash

Retries reuse the same logical order identity.

Never create a new order merely because an HTTP/API call timed out.

## Unknown-order state

If ASTRA submits an order but does not receive a reliable response:

DO NOT immediately retry as a new order.

Mark:
UNKNOWN_SUBMISSION

Then:
1. query broker order book using available identifiers/context
2. reconcile positions/open orders
3. resolve to ACKNOWLEDGED/FILLED/REJECTED/NOT_FOUND
4. only resubmit after deterministic proof that no original order exists

Unknown state blocks conflicting orders when duplication could increase risk.

## Order state machine

INTENT_CREATED
-> RISK_ACCEPTED
-> SUBMITTING
-> ACKNOWLEDGED
-> PARTIALLY_FILLED
-> FILLED

Alternate:
-> REJECTED
-> CANCEL_PENDING
-> CANCELLED
-> EXPIRED
-> UNKNOWN_SUBMISSION
-> RECONCILIATION_REQUIRED

Every transition:
- append-only audit event
- event timestamp
- source
- broker identifiers
- previous/new state

Invalid transitions are rejected.

## Startup/restart reconciliation

On every process start:
1. LIVE execution starts disabled
2. authenticate
3. retrieve broker positions
4. retrieve open/pending orders
5. retrieve recent completed orders/trades
6. compare with ASTRA persisted state
7. resolve mismatches
8. calculate actual portfolio exposure
9. run risk engine
10. enable order submission only if reconciliation passes

A process restart must never assume yesterday/in-memory state is correct.

## Periodic reconciliation

During market hours periodically compare:
- ASTRA orders vs broker orders
- ASTRA fills vs broker trade book
- ASTRA positions vs broker positions
- ASTRA cash/margin vs broker values

Mismatch severity:
INFO
WARNING
BLOCK_NEW_ORDERS
EMERGENCY

Material unresolved mismatch blocks new exposure.

## Stale-data guard

Every market-data object has:
- event timestamp
- receive timestamp
- age

Before execution:
- price must be fresh
- instrument master must be current
- market session must be open/valid
- spread/liquidity observations must be fresh

If data age exceeds strategy-specific limits:
REJECT_ORDER_INTENT

Do not trade from cached stale prices after reconnect.

## Circuit breakers / kill switches

### Strategy kill switch
Disables one strategy.

### Instrument/underlying kill switch
Disables new risk in one symbol/underlying.

### Broker kill switch
Stops all new submissions to one broker.

### Global kill switch
Stops all new exposure.

Kill switches must:
- persist across restart
- be checked immediately before submission
- default to safe state when configuration is corrupted

Emergency policy should distinguish:
STOP_NEW_ORDERS
from
FLATTEN_POSITIONS

Flattening itself carries execution risk and should not be blindly triggered for every software fault.

## Pre-trade checks

Immediately before every broker call revalidate:
- LIVE mode enabled
- kill switch off
- authenticated session valid
- static-IP/execution environment correct
- market/session valid
- instrument valid
- quantity/lot valid
- fresh market data
- position limits
- open-risk limits
- daily loss
- drawdown throttle
- Greek limits
- margin/capital reserve
- duplicate/client_order_id
- rate limits

Signal approval earlier in the pipeline is insufficient; risk must be checked again at execution time.

## Rate limiting

Implement:
- broker-specific request budgets
- exchange/order-rate constraints
- token bucket/leaky bucket limiter
- separate limits for order vs market-data endpoints
- exponential backoff for retry-safe requests
- no blind retry for non-idempotent transactional requests

Priority:
1. risk-reducing cancels/exits
2. reconciliation
3. new entries

## Authentication/token lifecycle

Broker sessions/tokens can expire daily.

Rules:
- credentials never stored in code/repo
- session status visible
- pre-market authentication/reconciliation
- session-expiry detection
- no automatic workaround for mandatory user/broker authentication
- expired authentication blocks new orders

## Secret isolation

Never commit:
- API key
- API secret
- broker token
- password
- MPIN
- TOTP seed
- OAuth token
- INDmoney credentials
- cookies
- private keys

Use:
- environment/secret manager
- least-privilege filesystem permissions
- encryption at rest where appropriate
- rotation after suspected exposure
- separate development/paper/live credentials

Logs must redact secrets.

## GitHub policy

Repository contains:
- source code
- schemas
- tests
- sample config without real values

Repository must not contain:
- .env with secrets
- broker databases
- token caches
- credential backups
- production SSH keys

Secret scanning and dependency scanning should be enabled where available.

## Network/server security

Production host:
- static IPv4 where broker rules require it
- minimal exposed ports
- firewall default deny
- SSH key authentication
- disable direct root login where practical
- patch OS/dependencies
- HTTPS/TLS
- rate limit/login protections
- TOTP/strong admin authentication
- restricted admin access
- encrypted backups
- monitoring/log rotation

Do not expose OpenAlgo/ASTRA's application port directly to the public internet when a hardened reverse-proxy/private-access design can be used.

## Broker API boundary

ASTRA should call a narrow execution adapter, not scatter broker calls across strategy code.

Interface examples:
- place_order(intent)
- cancel_order(id)
- modify_order(id, changes)
- fetch_orders()
- fetch_trades()
- fetch_positions()
- fetch_funds()
- health_check()

Broker-specific quirks are normalized inside adapters.

## Failure classes

### Safe transient
Example:
market-data request timeout

Action:
retry with backoff if idempotent.

### Ambiguous transactional
Example:
order POST timed out after request left server

Action:
UNKNOWN_SUBMISSION + reconcile; do not blindly retry.

### State divergence
Example:
broker shows position ASTRA does not know about

Action:
block new exposure + reconcile.

### Risk-critical
Example:
unexpected position exceeds hard limit

Action:
global/underlying kill switch; alert; use explicit risk-reduction procedure.

### Infrastructure security
Example:
suspected credential compromise

Action:
disable live, revoke/rotate credentials, reconcile account, preserve audit logs.

## Observability

Metrics:
- broker latency
- market-data age
- order acknowledgement latency
- rejection rate
- partial-fill rate
- reconciliation mismatches
- reconnect count
- duplicate prevention events
- realized slippage
- API error rate
- risk-limit rejections
- kill-switch state

Alerts should be actionable, not noisy.

## Audit trail

Append-only record for:
- input market event reference
- signal
- strategy version
- feature snapshot/hash
- risk decision
- order intent
- broker request/response metadata
- state transitions
- fills
- portfolio state
- manual intervention

Sensitive values are redacted.

Audit records should make it possible to reconstruct why every live order existed.

## Deployment change control

No direct untested production updates.

Code path:
research branch
-> tests
-> review
-> paper/shadow environment
-> tagged release
-> production

Live server records exact git commit/tag.

Rollback must be supported.

## Dependency / supply-chain risk

For third-party libraries:
- pin versions
- maintain lockfile
- review critical upgrades
- dependency scanning
- minimize unnecessary packages
- prefer maintained libraries
- verify installation sources

Never run arbitrary GitHub trading code with live credentials before review.

## Security testing

Before LIVE:
- unit tests for state transitions
- duplicate-submit tests
- network timeout tests
- broker response corruption tests
- process crash/restart tests
- stale-data tests
- token-expiry tests
- reconciliation mismatch tests
- kill-switch tests
- rate-limit tests
- secret-leak scan

## Initial ASTRA live policy

First production-capable version should still default to PAPER.

Required progression:
PAPER
-> SHADOW
-> LIMITED_LIVE

LIMITED_LIVE:
- smallest practical risk
- defined-risk structures preferred
- strict daily loss
- strict total exposure
- human-visible alerts
- no autonomous strategy self-modification

Scale only after replay/paper/shadow/live behavior is consistent.

## Key principle

The execution engine is successful when failures make ASTRA trade LESS, not MORE.

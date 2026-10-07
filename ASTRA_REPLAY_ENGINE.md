# ASTRA Historical Replay & Backtesting Engine

Status: research/design only. No live execution changes.

## Objective

ASTRA's replay engine must answer one question:

Could this strategy have produced these results using only information available at the time, at prices and costs that were realistically tradable?

If not, the backtest is invalid.

## Core architecture

historical / recorded market data
-> deterministic event clock
-> market-data event
-> feature update
-> strategy evaluation
-> signal intent
-> portfolio/risk checks
-> order intent
-> simulated venue/broker
-> fills / rejects / cancels / partial fills
-> portfolio accounting
-> journal / metrics

The same strategy and order-state interfaces should later be reusable in paper, shadow and live modes.

## Event ordering

Within the same timestamp, use a documented deterministic order:

1. session/exchange state event
2. instrument/master/corporate event effective at that instant
3. market-data update
4. derived feature update
5. strategy callback
6. risk evaluation
7. order submission
8. simulated acknowledgement
9. fill/reject/cancel/partial fill
10. portfolio/account update
11. strategy fill callback
12. journal snapshot

A strategy must never fill at a price that occurred before its order became eligible.

## OHLC bar replay rules

Bar data does not reveal the exact intrabar path.

Default policy:
- strategy sees a completed bar only after close
- orders generated from the bar are eligible from the next event/bar
- do not assume a favorable same-bar fill
- if both stop and target are touched in one bar and the path is unknown, use a conservative ambiguity policy or mark the event unresolved
- path-sensitive strategies require finer-grained data

Forbidden example:
Signal generated from today's close, then filled at today's low.

## Quote/tick replay

Where quote/tick data exists:
- maintain best bid/ask
- timestamp events strictly
- market BUY crosses the ask
- market SELL crosses the bid
- limit fills require an executable opposite-side price
- stale quotes cannot fill orders
- crossed/invalid markets are quarantined
- optionally model queue/size constraints when depth data exists

## Order lifecycle

Every simulated order should pass through explicit states such as:

CREATED
-> RISK_ACCEPTED
-> SUBMITTED
-> ACKNOWLEDGED
-> PARTIALLY_FILLED
-> FILLED

or

-> REJECTED
-> CANCEL_PENDING
-> CANCELLED
-> EXPIRED

State transitions must be idempotent and logged.

## Partial fills

A backtest must not assume unlimited liquidity.

Possible models by data quality:

### Bar-only
Use volume participation caps and conservative fill prices.

### Quote data
Cap fill size by visible quote quantity.

### Order-book data
Model fills across price levels and queue assumptions.

ASTRA should report how much P&L depends on optimistic liquidity assumptions.

## Slippage models

Support at least:
- fixed ticks
- fixed basis points
- half-spread / full-spread
- volatility-scaled
- participation/impact model
- instrument-specific empirical model

Every strategy must be stress-tested at worse-than-baseline slippage.

## Indian transaction-cost engine

Costs must be versioned by effective date.

Model separately:
- brokerage
- STT
- exchange transaction charges
- SEBI turnover fees
- GST
- stamp duty
- other applicable statutory levies

Do not hardcode one timeless percentage.

For equity derivatives, ASTRA must use date-effective STT rules. From 1 April 2026, NSE publishes:
- option sale STT: 0.15% of option premium
- exercised option STT: 0.15% on intrinsic value, payable by purchaser
- futures sale STT: 0.05% of traded value

Historical simulations before that date must use the earlier rates.

## Expiry and settlement

Expiry is a first-class event.

Replay engine must know:
- instrument expiry timestamp/date
- last tradable session
- whether position is closed, expires worthless or settles
- final settlement price rule
- exercise/intrinsic value
- settlement-day costs/taxes
- historical contract specifications

Never carry an expired contract forward as if it were still tradable.

Expiry-sensitive strategies must be tested separately from normal sessions.

## Options-specific execution

For each candidate option trade, replay should include:
- exact contract identity
- underlying price
- strike
- expiry
- option type
- bid/ask
- spread
- volume
- OI
- lot size
- tick size
- time to expiry
- IV/Greeks version and timestamp

Contract selection must happen using only the chain/contracts visible at decision time.

## Stops and targets

Stops/targets are orders, not magical prices.

Model:
- trigger condition
- order submission after trigger
- gap-through behavior
- next available executable price
- partial fills where applicable

A stop at 100 does not guarantee a 100 fill.

## Latency

Replay should permit configurable:
- market-data latency
- strategy compute latency
- risk-check latency
- broker/API latency
- exchange acknowledgement latency

Even if v1 uses simple constants, latency must exist explicitly in the model.

## Rejections and failures

Test:
- exchange/broker rejection
- invalid quantity/lot
- insufficient margin
- stale instrument master
- order timeout
- duplicate submission
- disconnect
- reconnect and reconciliation
- missing quote

A strategy that only works when every order succeeds is not production-ready.

## Margin / capital

Replay must track:
- available cash
- blocked margin
- realized P&L
- unrealized P&L
- fees/taxes
- exposure
- open risk
- collateral assumptions where applicable

Never size trades from future end-of-day equity.

## Accounting invariants

At every event:
cash + marked positions - liabilities - costs = account equity

Reconciliation failures should fail the simulation rather than silently continue.

## Corporate actions and contract changes

For equities:
- splits
- bonuses
- dividends
- symbol changes
- index membership changes

For derivatives:
- lot size changes
- strike intervals
- expiries
- contract specification changes

All must be effective-dated.

## Validation tiers

### Tier 1 — bar replay
Good for:
- daily momentum
- coarse trend
- regime filters
- low-turnover strategies

### Tier 2 — intraday quote replay
Needed for:
- intraday index strategies
- spread-sensitive options
- realistic stop/limit behavior

### Tier 3 — order-book replay
Needed for:
- microstructure
- latency-sensitive strategies
- queue/impact studies
- expiry-day scalping

Do not claim Tier-3 realism from Tier-1 data.

## Backtest report requirements

Every run must report:
- gross P&L
- net P&L
- all fees/taxes
- spread cost
- slippage cost
- rejected orders
- partial fills
- turnover
- max drawdown
- exposure
- number of trades
- expectancy
- Sharpe/Sortino
- profit factor
- results by regime
- results by expiry distance
- liquidity bucket
- slippage sensitivity
- unresolved intrabar events

## Reality-gap tests

Before promotion, compare:
historical replay vs paper vs shadow-live.

Track:
- signal timing differences
- fill-price differences
- fill-rate differences
- latency
- realized spread/slippage
- rejected orders
- P&L divergence

If live-like modes consistently underperform replay beyond tolerance, the strategy is demoted for model recalibration.

## ASTRA replay policy

A backtest is not a prediction.

It is an audit of whether a fixed trading process would have survived historical market events under explicit assumptions.

Optimistic assumptions are not allowed to remain implicit.

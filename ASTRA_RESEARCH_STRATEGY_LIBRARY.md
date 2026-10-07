# ASTRA Trader — Strategy Library Research

Status: research/design only. No live execution changes.

## Repositories/frameworks worth learning from

### Event-driven production engines
- nautechsystems/nautilus_trader — deterministic event-driven backtest/live architecture, order/execution state, persistence.
- QuantConnect/Lean — research/backtest/live separation, brokerage abstractions, options/futures support.
- AsyncAlgoTrading/aat — smaller event-driven architecture reference.

### Fast research/backtesting
- polakowo/vectorbt — fast vectorized signal/parameter exploration.
- kernc/backtesting.py — compact strategy/backtest model useful for prototyping.
- mementum/backtrader — order simulation, commissions, slippage, multi-timeframe patterns.

### Portfolio/risk construction
- PyPortfolio/PyPortfolioOpt — efficient frontier, Black-Litterman and allocation utilities.
- dcajasn/Riskfolio-Lib — risk parity, hierarchical and multiple risk-measure portfolio optimization.

### Indian market / options references
- marketcalls/openalgo — Indian broker abstraction and execution connectivity.
- marketcalls/opengreeks — options pricing, IV and higher-order Greeks.
- rajmaurya0904/bhav — NSE options backtesting/replay concepts.
- Dhan/NIFTY-oriented strategy labs — Indian costs, expiry and paper-validation patterns.

## What ASTRA should borrow

1. One canonical event model for historical replay, paper and live.
2. Deterministic order and position state machines.
3. Explicit data timestamps and no look-ahead access.
4. Realistic fees, spread, slippage, latency and rejection models.
5. Portfolio-level exposure/risk limits independent of strategies.
6. Fast vectorized research, followed by slower event-driven confirmation.
7. Options chain normalization with OI, IV, Greeks, expiry, liquidity and spread.
8. Reproducible experiment manifests and immutable strategy versions.
9. Walk-forward/out-of-sample promotion gates.
10. Crash-safe reconciliation and idempotent order submission.

## Strategy families to research before implementation

### Trend / momentum
- multi-timeframe trend
- breakout / volatility expansion
- relative strength
- time-series momentum

### Mean reversion
- VWAP/anchored VWAP reversion
- z-score/statistical reversion
- intraday overextension
- pairs/spread reversion

### Volatility / options
- IV vs realized volatility
- skew / term structure
- delta-defined option selection
- vertical spreads
- calendars
- defined-risk premium selling
- gamma/convexity event setups

### Market microstructure / derivatives context
- OI and OI-change
- futures basis
- PCR as context, not standalone signal
- bid/ask spread and depth
- liquidity and impact filters

### Regime layer
- trend/range
- low/high volatility
- risk-on/risk-off
- event/expiry regime
- change-point/HMM-style regime classification as a filter, not an oracle

## Non-negotiable validation

A strategy cannot progress to live simply because it has a high win rate.

Required:
- positive expectancy after all costs
- adequate trade count
- out-of-sample profitability
- walk-forward stability
- parameter robustness
- slippage sensitivity tests
- Monte Carlo drawdown analysis
- regime attribution
- concentration checks
- maximum drawdown limits
- paper/shadow performance agreement

## Current ASTRA build policy

Research -> Prototype -> Fast backtest -> Event-driven replay -> OOS -> Walk-forward -> Monte Carlo -> Paper -> Shadow -> Small live allocation -> Scale.

AI may rank, research, explain and propose candidate changes. It may not override deterministic risk controls or promote an unvalidated strategy directly into production.

# ASTRA Alpha Validation & Anti-Overfitting Research

Status: research/design only. No live trading changes.

## Core principle

ASTRA must optimize for repeatable out-of-sample expectancy, not maximum historical return or win rate.

## Alpha research workflow

1. State an economic/market hypothesis before tuning parameters.
2. Define features using only information available at decision time.
3. Split development data from untouched validation data.
4. Use fast research tools for exploration, but log every trial.
5. Confirm finalists in an event-driven simulator with realistic costs/fills.
6. Run rolling/anchored walk-forward tests.
7. Run Monte Carlo / trade-sequence resampling.
8. Evaluate performance by regime and instrument.
9. Paper trade and then shadow-live before any capital allocation.
10. Promote only immutable, versioned strategy builds.

## Metrics beyond win rate

- expectancy
- profit factor
- Sharpe / Sortino
- Deflated Sharpe Ratio
- maximum drawdown
- Calmar
- tail loss / CVaR
- turnover and cost drag
- exposure time
- hit rate by regime
- average adverse/favorable excursion
- parameter stability
- out-of-sample degradation
- strategy correlation to other ASTRA strategies

## Multiple-testing control

ASTRA must record:
- number of strategy variants tried
- parameter grids / optimization trials
- datasets and windows used
- objective functions tried
- discarded variants

A strong backtest after hundreds or thousands of experiments is less convincing than the same result from a small pre-specified search. Use Deflated Sharpe-style correction and overfitting diagnostics before promotion.

## Time-series leakage controls

Use time-aware validation only.

Required where applicable:
- chronological train/validation/test splits
- purging around overlapping labels/trades
- embargo periods around fold boundaries
- no random K-fold CV for serial market data when it leaks future/overlapping information
- feature timestamps stored explicitly
- point-in-time data versions

## Walk-forward policy

ASTRA should support rolling and anchored walk-forward testing.

For each fold:
- optimize only on past data
- freeze parameters
- test on the immediately following unseen interval
- log OOS returns independently
- roll forward and repeat

Promotion should favor consistency across OOS windows rather than one exceptional period.

## Robustness tests

A candidate should survive:
- nearby parameter perturbations
- increased commissions
- wider spreads
- worse slippage
- delayed entries
- partial-fill assumptions
- missing data
- different start/end dates
- regime subsets
- shuffled/resampled trade sequences

Reject strategies that require one exact parameter combination or collapse under modest friction changes.

## Regime research

Regime classification is a filter, not a prediction oracle.

Potential inputs:
- realized volatility
- ATR / range expansion
- trend strength
- breadth
- correlation
- futures basis
- IV level / percentile
- skew
- term structure
- liquidity/spread
- event/expiry calendar

Candidate methods:
- deterministic rule-based regimes
- clustering
- Hidden Markov Models
- change-point detection
- tree/boosting classifiers trained only on past information

Always compare a regime-aware system against a simpler non-regime baseline.

## Alpha feature families

Price/return:
- multi-horizon returns
- breakout distance
- trend slope
- z-score / overextension
- gap and overnight effects

Volume/liquidity:
- volume surprise
- relative volume
- spread
- depth / impact proxy
- turnover

Derivatives:
- futures basis
- OI and OI change
- option volume
- IV / IV rank / IV percentile
- skew / term structure
- delta/gamma/theta/vega
- higher-order Greeks only where economically useful
- expiry/time-to-expiry

Cross-sectional:
- relative strength
- breadth
- sector/index relative performance
- dispersion
- correlation structure

Calendar/event:
- expiry
- RBI/Fed or major scheduled events
- earnings/corporate events for single stocks
- open/close/session effects

## Portfolio combination

Do not simply add all profitable strategies.

For each strategy, estimate:
- return correlation
- drawdown correlation
- exposure overlap
- common factor/regime dependence
- tail-loss coincidence

Possible allocation methods to research:
- equal risk contribution
- inverse volatility
- risk parity
- hierarchical risk parity
- constrained mean-variance / Black-Litterman
- volatility targeting

Hard portfolio constraints remain outside optimization.

## Strategy promotion states

RESEARCH
-> VALIDATED
-> PAPER
-> SHADOW
-> LIMITED_LIVE
-> PRODUCTION

Automatic demotion triggers should include:
- drawdown breach
- expectancy deterioration
- abnormal slippage
- regime mismatch
- data integrity failure
- broker/reconciliation failure

No AI component may skip a state or override a risk/demotion rule.

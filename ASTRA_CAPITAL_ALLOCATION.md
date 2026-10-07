# ASTRA Capital Allocation & Portfolio Risk

Status: research/design only. No live trading changes.

## Objective

ASTRA should allocate capital across simultaneous signals and strategies while controlling:
- total portfolio risk
- correlated exposure
- concentration
- leverage
- drawdown
- tail risk
- liquidity risk
- options Greeks
- strategy overlap

The portfolio/risk layer is independent of strategy logic and cannot be overridden by AI.

## Allocation philosophy

Do not optimize for maximum historical return.

Prefer robust risk allocation methods such as:
- equal risk contribution
- inverse volatility
- hierarchical risk parity
- hierarchical equal risk contribution
- minimum variance / downside-risk variants
- constrained mean-variance only when expected-return estimates are demonstrably stable

Expected-return estimates are noisy. ASTRA should default toward risk-focused allocation and require strong evidence before using return forecasts aggressively.

## Signal-to-capital pipeline

candidate signals
-> strategy-level risk estimate
-> normalize to comparable risk units
-> correlation / exposure clustering
-> portfolio constraints
-> capital allocator
-> deterministic risk checks
-> order sizing
-> execution

## Position sizing

ASTRA should support multiple sizing models but none may bypass hard limits.

Research candidates:
- fixed fractional risk
- volatility targeting
- ATR/range-based sizing
- inverse volatility
- fractional Kelly as an upper-bound reference only
- option-loss-defined sizing for defined-risk structures

Default live philosophy:
- conservative fixed-fractional risk
- volatility adjustment
- portfolio-level cap

Full Kelly should not be used because estimation error can create extreme allocations.

## Hard portfolio constraints

Examples:
- max risk per trade
- max total open risk
- max gross exposure
- max net directional exposure
- max leverage
- max strategy allocation
- max instrument allocation
- max underlying allocation
- max sector allocation
- max expiry concentration
- max correlated-cluster exposure
- max daily loss
- max rolling drawdown
- max tail-risk budget
- liquidity participation cap

These limits are checked after optimization, not left to the optimizer.

## Correlation and hidden duplication

Two strategies can look different but carry the same economic risk.

ASTRA should estimate:
- return correlation
- drawdown correlation
- same-side underlying exposure
- sector/index beta
- volatility beta
- options Greek overlap
- common regime dependence
- timing overlap

Examples:
- long NIFTY futures + multiple bullish NIFTY call trades = duplicated delta risk
- long BANKNIFTY calls + bullish bank-stock positions = concentrated banking beta
- several short-volatility option structures = duplicated short-vega/tail risk

Allocation must cluster or penalize these overlaps.

## Strategy allocation

Each strategy receives a risk budget rather than a fixed rupee budget.

Possible allocation frameworks:
- equal strategy risk
- inverse-volatility strategy risk
- hierarchical clustering of strategy returns
- drawdown-aware weighting
- regime-conditioned caps

A strategy with rising volatility or worsening drawdown gets less risk even if its nominal signal strength is unchanged.

## Drawdown throttling

Portfolio risk should decrease automatically during drawdown.

Example policy to research:
- 0–3% drawdown: normal risk
- 3–5%: reduce risk
- 5–8%: stronger reduction
- >8%: halt new risk / require review

Exact thresholds must be validated; the important point is monotonic risk reduction during stress.

Drawdown throttle must act on:
- account level
- strategy level
- correlated strategy cluster level

## Loss-streak controls

Loss streak alone does not prove a strategy is broken, but it is useful operationally.

Track:
- consecutive losses
- rolling expectancy
- rolling hit rate
- rolling profit factor
- realized vs expected slippage
- live vs replay divergence

Use these jointly rather than disabling solely after N losses.

## Volatility targeting

ASTRA can scale exposure toward a target portfolio volatility.

Requirements:
- robust volatility estimator
- cap leverage
- slow enough adjustment to avoid turnover explosion
- emergency override in volatility spikes

Do not mechanically lever low-volatility periods without strict leverage and liquidity limits.

## Portfolio covariance

For multi-asset/strategy allocation, research:
- shrinkage covariance
- exponentially weighted covariance
- robust covariance
- hierarchical clustering

Sample covariance alone can be unstable.

PyPortfolioOpt explicitly supports covariance shrinkage and Hierarchical Risk Parity, while Riskfolio-Lib exposes multiple downside, tail and drawdown risk measures.

## Options portfolio risk

Options require risk aggregation beyond premium paid.

Track at underlying and portfolio levels:
- delta
- gamma
- vega
- theta
- optionally vanna/charm where useful
- max defined loss
- scenario loss
- expiry concentration

Possible constraints:
- max absolute delta
- max gamma near expiry
- max negative vega
- max short convexity
- max same-expiry risk
- max uncovered option risk

Defined-risk option spreads should be preferred in early live stages.

## Scenario stress tests

Before accepting a portfolio, evaluate shocks such as:
- index +/-1%, +/-2%, +/-5%
- volatility +/− specified points
- gap scenarios
- correlation spike
- liquidity deterioration
- adverse overnight move
- expiry-day gamma move

For options, scenario P&L is often more informative than a single variance estimate.

## Tail-risk budget

Track:
- historical CVaR / expected shortfall
- worst-case scenario loss
- drawdown risk
- gap risk

Riskfolio-Lib is a useful reference because it supports CVaR, EVaR, tail-Gini and drawdown-oriented measures.

## Liquidity sizing

Position size must also satisfy:
- max fraction of observed volume
- max spread threshold
- minimum OI for derivatives
- quote depth where available
- conservative unwind capacity

ASTRA should size for the exit, not only the entry.

## Capital reservation

Keep unallocated capital for:
- margin variation
- slippage
- gap risk
- broker/exchange margin changes
- emergency exits

Do not run the account at theoretical maximum margin utilization.

## Multiple simultaneous signals

When signals compete for limited risk budget:

1. reject any signal failing hard risk filters
2. group correlated exposures
3. estimate incremental portfolio risk
4. rank by validated strategy quality / expected risk-adjusted edge
5. allocate within cluster and portfolio caps
6. re-run portfolio stress tests
7. submit only orders that keep all constraints satisfied

A high score does not guarantee an allocation if it duplicates existing risk.

## Rebalancing policy

Avoid excessive optimization churn.

Research:
- minimum weight-change threshold
- rebalance bands
- transaction-cost-aware optimization
- cooldown periods

Optimization benefit must exceed estimated trading costs.

## References and design inputs

### PyPortfolioOpt
Useful for:
- covariance shrinkage
- minimum variance
- Black-Litterman
- Hierarchical Risk Parity
- constrained optimization

Its own documentation warns that expected returns are difficult to forecast and notes risk-focused approaches such as minimum variance and HRP as robust alternatives to naive max-Sharpe use.

### Riskfolio-Lib
Useful for:
- HRP/HERC
- CVaR and other downside risk measures
- tail-risk measures
- drawdown-based risk optimization

## ASTRA initial allocation policy

For first paper-trading versions:

1. fixed fractional risk per trade
2. inverse-volatility adjustment
3. underlying/sector/correlation caps
4. total open-risk cap
5. options Greek limits
6. drawdown throttle
7. liquidity cap
8. hard daily-loss kill switch

Advanced portfolio optimization should remain research-only until the simpler allocator has a reliable OOS and paper-trading baseline.

## Promotion rule

A more complex allocator must outperform the simple baseline after:
- costs
- turnover
- drawdowns
- tail scenarios
- OOS testing

Complexity without stable incremental benefit is rejected.

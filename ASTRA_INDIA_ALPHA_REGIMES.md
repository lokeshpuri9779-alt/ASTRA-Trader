# ASTRA India Alpha & Regime Research

Status: research/design only. No live execution changes.

## Principle

ASTRA must distinguish between:
1. primary alpha features,
2. contextual derivatives features,
3. structural exchange/expiry mechanics,
4. machine-learned regime labels.

No single OI, PCR, RSI, IV or HMM output is allowed to act as a standalone trade trigger.

## Primary feature hierarchy

### Tier 1 — price/trend/volatility
These are the first features to test because they are closest to actual price formation.

- multi-horizon return
- breakout distance
- trend slope
- realized volatility
- ATR / range expansion
- gap / overnight return
- intraday VWAP distance
- relative volume
- breadth / relative strength

### Tier 2 — derivatives context
Useful as confirmation, regime information, or instrument-selection features.

- futures basis
- option OI by strike
- OI change
- option volume
- IV
- IV rank / percentile
- skew
- term structure
- delta / gamma / theta / vega
- bid/ask spread
- liquidity / depth proxies
- PCR

Rules:
- OI is not directional by itself.
- PCR is contextual, not a buy/sell switch.
- IV should be compared with realized volatility and its own history.
- Greeks must be interpreted with time-to-expiry and spot/volatility changes.

## Indian market regime model

ASTRA should initially use a transparent rule-based regime baseline before introducing ML.

Suggested baseline states:
- TREND_LOW_VOL
- TREND_HIGH_VOL
- RANGE_LOW_VOL
- RANGE_HIGH_VOL
- EVENT
- EXPIRY

Candidate inputs:
- NIFTY return/trend
- realized volatility
- India VIX
- ATR percentile
- breadth
- futures basis
- option IV percentile
- skew
- liquidity/spread
- days/minutes to expiry
- scheduled macro/event calendar

ML/HMM/clustering can later classify regimes, but every ML regime model must beat the simpler rule-based baseline OOS.

## Momentum / trend research

Research candidates:
- 3/6/12-month cross-sectional momentum for equity selection
- short-horizon time-series momentum for indices/futures
- breakout + volatility expansion
- relative-strength ranking within NIFTY / sector universe
- trend filters combined with volatility targeting

Avoid:
- choosing one lookback because it maximizes historical CAGR
- survivorship-biased current-index constituents
- overlapping train/test leakage

## Mean-reversion research

Research candidates:
- VWAP/anchored-VWAP deviation
- intraday z-score overextension
- gap mean reversion conditioned on regime
- pairs/spread reversion

Mean reversion should be disabled or strongly penalized in persistent trend/high-volatility regimes unless independently validated.

## Options / volatility research

Research candidates:
- IV minus realized volatility
- IV percentile / rank
- skew steepening/flattening
- front-vs-back expiry term structure
- delta-defined contract selection
- vertical spreads
- calendar spreads
- defined-risk premium strategies
- event-volatility setups
- gamma-sensitive intraday setups near expiry

All options research must include:
- strike-level liquidity
- spread
- exact expiry
- time-to-expiry
- realistic entry/exit fills
- brokerage/fees/taxes
- assignment/settlement assumptions where relevant
- contract-lot changes and historical contract specifications

## OI interpretation

Possible contextual patterns to test:
- price up + OI up
- price up + OI down
- price down + OI up
- price down + OI down

These are hypotheses only. ASTRA must validate their predictive value by instrument, horizon, expiry distance and regime.

Strike-level OI should be normalized relative to:
- nearby strikes
- prior observations
- total chain OI
- distance from spot
- expiry

## Expiry regime

Expiry trading must be treated as a distinct regime rather than pooled with normal sessions.

Features:
- minutes/days to expiry
- ATM gamma concentration
- spread/liquidity
- IV crush/expansion
- strike migration around spot
- OI concentration
- realized intraday volatility
- order-book quality

Strategies validated on ordinary sessions cannot automatically trade expiry sessions.

## Regime detection research

Reference implementation patterns found on GitHub include Indian-market experiments using NIFTY 50 + India VIX with K-means and Gaussian HMMs.

ASTRA policy:
1. build rule-based baseline first,
2. add HMM/clustering model,
3. use forward-filtered states only,
4. perform chronological/OOS evaluation,
5. compare against no-regime and rule-based baselines,
6. reject if complexity does not add stable OOS value.

## GitHub references inspected

- jhambaarav/nifty50-momentum-strategy
  - example of rules-based 6-month momentum research on NIFTY 50 with an ML selection layer.
  - useful as a hypothesis/example, not proof of durable alpha.

- ashok-kollipara/options-oi
  - NIFTY/BANKNIFTY option-chain OI tooling.
  - useful for data/visualization patterns; OI is contextual, not a standalone edge.

- kharepk13/Calculating-option-volatility-for-NIFTY-Options
  - NIFTY option IV calculation example.
  - useful for basic implementation reference; ASTRA should use a stronger audited Greeks/IV layer.

- reshmasayyad/market-regime-detection
  - Indian equity regime-detection experiment using NIFTY 50, India VIX, K-means and Gaussian HMMs with chronological evaluation.
  - useful reference for forward-only regime labeling.

## Promotion requirements for any India-specific alpha

A candidate must show:
- positive net expectancy after Indian trading costs
- OOS performance
- walk-forward consistency
- robustness to worse spreads/slippage
- stability across multiple market regimes
- no single expiry/event period dominating returns
- enough independent trades
- drawdown within risk budget
- no hidden dependence on current index constituents
- clear timestamp/point-in-time data provenance

## Initial ASTRA research priority

1. NIFTY/BANKNIFTY trend + volatility regime baseline
2. relative-strength equity momentum
3. options-chain normalization
4. IV-vs-realized-volatility features
5. OI/PCR contextual overlays
6. expiry-specific regime
7. options spread research
8. ML/HMM regime layer only after baseline validation

# ASTRA Automated Research Factory

Status: research/design only. No autonomous deployment or live trading changes.

## Objective

ASTRA should automate research throughput without automating self-deception.

The research factory may:
- generate hypotheses
- queue experiments
- run backtests
- run robustness tests
- score candidates
- reject weak/overfit ideas
- surface a small shortlist

It may not:
- promote directly to live
- hide failed trials
- rewrite pass criteria after seeing results
- optimize on the final held-out test window
- bypass validation gates

## Research object model

Each hypothesis gets a permanent ID before testing.

Hypothesis record:
- hypothesis_id
- created_at
- economic rationale
- market/instruments
- expected regime
- signal definition
- holding horizon
- allowed parameter ranges
- primary metric
- pass/fail thresholds
- data window policy
- cost/slippage assumptions
- maximum experiment budget
- author/source
- status

The pass criteria are locked before the first backtest.

## Pre-registration

ASTRA should support lightweight pre-registration.

Before testing:
- define what would count as success
- define what would count as failure
- define allowed tuning range
- define validation method
- define final untouched OOS window

If thresholds are changed after results are seen, create a new hypothesis version and count prior trials.

## Hypothesis generation

Sources:
- known market effects
- strategy research papers
- GitHub implementations
- exchange microstructure
- observed regime behavior
- failed-strategy diagnostics
- feature interaction ideas
- AI-generated hypotheses

AI-generated ideas receive no credibility bonus.

Each hypothesis should include a falsifiable rationale such as:
"Breakouts accompanied by volatility expansion and relative-volume confirmation may persist longer in TREND_HIGH_VOL regimes."

Avoid:
"Use RSI 37 because that backtested best."

## Experiment queue

Experiment types:
- baseline
- parameter perturbation
- alternate universe
- alternate horizon
- alternate regime
- cost stress
- slippage stress
- delayed entry
- walk-forward
- purged CV / CPCV
- Monte Carlo
- feature ablation
- placebo/null test

Queue priority should favor information gain, not only candidates with highest preliminary return.

## Trial accounting

Count every attempted strategy/model configuration.

Record:
- successful trials
- failed trials
- crashed trials
- manually discarded trials
- alternate objectives tried
- parameter searches

This trial count feeds multiple-testing diagnostics such as Deflated Sharpe Ratio.

Deleting bad results is prohibited.

## Immutable result ledger

Every experiment creates an append-only result record:
- experiment_id
- hypothesis_id
- code commit
- dataset manifest
- parameter set
- seed
- start/end
- validation scheme
- costs
- metrics
- artifacts
- status
- failure reason

No result may be overwritten.

Reruns create new experiment IDs.

## Validation methods

Supported methods should include:

### Walk-forward
Rolling/expanding train window with immediately following OOS test.

### Purged K-fold
Remove overlapping-label observations around test folds.

### Embargo
Prevent nearby observations after test folds from leaking information.

### Combinatorial Purged CV
Generate multiple OOS paths instead of relying on one historical split.

Use only where mathematically appropriate for the labeling/horizon structure.

## Key statistical diagnostics

Candidate evaluation may include:
- Sharpe
- Probabilistic Sharpe Ratio
- Deflated Sharpe Ratio
- Minimum Track Record Length
- Probability of Backtest Overfitting
- bootstrap confidence intervals
- permutation/placebo tests
- Monte Carlo trade-sequence tests

No single statistic is sufficient.

## Final held-out window

Maintain a sealed final OOS window for important strategy families.

Rules:
- strategy development cannot repeatedly inspect it
- spend it only at a defined promotion milestone
- once examined, that window is no longer "unseen"
- future work needs a newer untouched period

## Baseline first

Every hypothesis must beat an appropriate simple baseline.

Examples:
- momentum model vs simple time-series momentum
- HMM regime strategy vs rule-based regime filter
- ML ranker vs raw factor ranking
- optimized portfolio vs inverse-vol/equal-risk baseline

Complexity that does not add stable OOS value is rejected.

## Feature ablation

For accepted candidates, rerun after removing feature groups.

Goal:
- identify whether performance depends on one fragile feature
- detect redundant features
- improve interpretability
- reduce unnecessary complexity

If removing a supposedly important feature does not change results, its role is questionable.

## Placebo and null tests

Examples:
- shuffled labels
- permuted signals
- randomized entry timestamps within valid constraints
- synthetic/noise features
- alternative universes with no expected effect

A research pipeline that "finds alpha" in placebo tests is suspect.

## Parameter robustness

Do not select only the single best point.

Inspect the parameter surface.

Prefer:
- broad stable plateaus

Reject:
- isolated sharp optimum
- boundary optimum with no economic explanation
- severe deterioration under nearby values

## Economic robustness

Stress:
- higher fees
- wider spread
- worse slippage
- entry delay
- smaller liquidity
- different start date
- different market regimes
- alternative instruments/universes

Edge should not disappear after modestly realistic perturbations.

## Candidate score

ASTRA can use a multi-dimensional research score, not one return metric.

Illustrative dimensions:
- OOS expectancy
- OOS risk-adjusted return
- drawdown
- stability across folds
- parameter robustness
- multiple-testing penalty
- cost/slippage resilience
- regime breadth
- strategy correlation/diversification value
- simplicity penalty
- data quality/confidence

The score ranks candidates; it does not override hard rejection criteria.

## Hard rejection criteria

Reject regardless of composite score if:
- data leakage detected
- final OOS materially fails
- net expectancy <= 0 after realistic costs
- drawdown exceeds mandate
- severe parameter instability
- result dominated by a few trades
- impossible fill assumptions
- hidden survivorship bias
- insufficient sample/track record
- strategy cannot be reproduced

## Research states

IDEA
-> PREREGISTERED
-> EXPLORING
-> ROBUSTNESS_TEST
-> OOS_VALIDATED
-> CANDIDATE

From CANDIDATE the existing deployment governance continues:
-> PAPER
-> SHADOW
-> LIMITED_LIVE
-> PRODUCTION

## Automated rejection

ASTRA should aggressively reject ideas.

A healthy research factory is expected to kill most hypotheses.

Useful output includes:
- why it failed
- which regime failed
- which assumption was fragile
- what feature added no value
- whether the hypothesis itself is falsified

Failed research remains searchable so ASTRA does not continually rediscover the same bad idea.

## Research memory

Maintain a structured knowledge base of:
- tested hypotheses
- null results
- parameter ranges already explored
- known leakage traps
- market regimes
- features that repeatedly fail
- successful combinations
- strategy correlations

Future hypothesis generation should consult this ledger.

## Parallelism

Safe to parallelize:
- independent parameter trials
- independent folds
- alternate universes
- stress tests

Not safe:
- mutating the same result/state concurrently
- changing shared live configuration
- using validation outputs to modify a still-running held-out test

## Compute budgeting

Each hypothesis gets a bounded experiment budget.

Budget can be increased only when preliminary evidence justifies more testing.

This limits brute-force data mining.

Track:
- CPU/GPU time
- trial count
- parameter count
- data windows touched

## Human review packet

The factory should eventually surface a concise candidate dossier:
- hypothesis/rationale
- strategy logic
- data provenance
- trial count
- OOS results
- walk-forward/CPCV distribution
- DSR/PBO diagnostics
- drawdown/tail risk
- cost/slippage stress
- regime attribution
- parameter surface
- placebo/ablation results
- portfolio correlation
- known failure modes
- exact code/data hashes

No "best strategy" screenshot without the audit packet.

## GitHub/design references

Useful research patterns:
- eslazarev/purged-cross-validation
  - purging, embargo, walk-forward, CPCV, PSR, DSR, minimum track-record/backtest-length tools
- Aliipou/backtest-audit
  - DSR, Probability of Backtest Overfitting and Monte Carlo permutation diagnostics
- DaruFinance/quant-research-framework
  - walk-forward, realistic frictions, robustness tests, Monte Carlo, overfitting statistics
- Finance-broski/nse-factor-backtest
  - NSE-oriented pre-registration, survivorship awareness, held-out testing, realistic costs and recording null results
- ndt93/FinancialML
  - financial ML research patterns including purged CV, labeling, feature importance and HRP

These are design references, not evidence that any included strategy will be profitable for ASTRA.

## Initial ASTRA research-factory implementation order

1. hypothesis schema
2. experiment manifest + append-only ledger
3. deterministic experiment runner
4. baseline/parameter sweep runner
5. walk-forward validation
6. purged/embargo CV
7. robustness and cost stress
8. Monte Carlo / placebo tests
9. trial-count-aware statistics
10. candidate dossier generator
11. research memory / duplicate-hypothesis detection
12. AI hypothesis generator last

## Core principle

Automate experimentation.
Automate rejection.
Do not automate belief.

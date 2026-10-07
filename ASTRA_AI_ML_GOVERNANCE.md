# ASTRA AI/ML Governance & Modeling

Status: research/design only. No live model control.

## Objective

AI/ML should improve research, ranking, regime classification, and anomaly detection without gaining authority over hard risk, broker controls, or deployment gates.

## What AI may do

Allowed roles:
- feature research
- signal ranking
- regime classification
- probability estimation
- anomaly detection
- slippage/impact estimation
- portfolio context summarization
- strategy attribution
- drift detection
- model diagnostics
- hypothesis generation
- natural-language explanations

## What AI may not do

AI/ML must not:
- override risk limits
- increase leverage beyond deterministic caps
- disable kill switches
- bypass broker/exchange rules
- change live secrets/authentication
- promote itself directly to production
- modify live parameters mid-session without a validated release
- place orders outside the deterministic execution gateway
- reinterpret failed reconciliation as safe

## Model hierarchy

Start simple and require incremental evidence for complexity.

Baseline order:
1. deterministic rules
2. linear/logistic models
3. tree/boosting models
4. probabilistic/state models
5. sequence/deep models only if they show stable OOS value

Every complex model must beat a simpler baseline after costs and stability tests.

## Prediction targets

Avoid vague targets like "market up".

Possible explicit targets:
- probability next-horizon return exceeds threshold
- expected return over fixed horizon
- probability of breakout continuation
- probability of mean reversion
- realized volatility forecast
- spread/slippage forecast
- regime probability
- probability trade hits stop before target

Targets must match execution horizon.

## Feature policy

Features must be:
- timestamped
- point-in-time available
- versioned
- economically interpretable where possible
- tested for leakage

Candidate feature groups:
- returns/trend
- volatility
- volume/liquidity
- derivatives context
- IV/skew/term structure
- OI/futures basis
- breadth/relative strength
- calendar/events
- portfolio state

## Feature leakage tests

Reject features that use:
- future close/high/low
- end-of-day values intraday before publication
- revised fundamentals unavailable then
- current index constituents historically
- labels overlapping improperly across CV folds
- future-normalized statistics

## Train/validation structure

Use chronological time-series splits.

Where labels overlap:
- purge overlapping samples
- embargo fold boundaries
- keep untouched final OOS period

Never use random K-fold for serial market data when it leaks temporal information.

## Probability calibration

For classifiers, ASTRA should evaluate:
- calibration curve
- Brier score
- log loss
- expected calibration error

A model predicting 70% confidence should be approximately right 70% of the time in comparable cases.

Signal strength should be derived from calibrated probabilities, not raw model scores.

## Ensemble design

Prefer diversified model ensembles rather than one monolithic model.

Possible ensemble:
- trend model
- mean-reversion model
- volatility model
- options-context model
- regime model

Meta-layer can combine them, but portfolio/risk limits remain external.

## Regime models

Candidate approaches:
- rule-based baseline
- HMM
- clustering
- change-point detection
- gradient boosting / trees

Use forward-only state inference.

A regime model may gate or reweight strategies, not guarantee direction.

## Drift detection

Track:
- feature distribution drift
- prediction distribution drift
- calibration drift
- realized-vs-predicted expectancy
- regime mix changes
- slippage drift
- fill-rate drift

Possible tools:
- PSI
- KS distance
- Wasserstein distance
- rolling calibration error
- rolling residual statistics

## Model lifecycle

RESEARCH
-> BACKTESTED
-> OOS_VALIDATED
-> PAPER
-> SHADOW
-> LIMITED_LIVE
-> PRODUCTION

Model version must be immutable within a live session.

## Retraining policy

No uncontrolled continuous self-learning with live money.

Retraining should happen:
1. offline
2. on a scheduled or evidence-triggered basis
3. with fixed data cut-off
4. with reproducible code/seed
5. with full validation
6. as a new version

New version must pass promotion gates before deployment.

## Champion / challenger

Maintain:
- champion = current approved model
- challenger = candidate model

Challenger can run in shadow mode.

Promote only if it materially improves:
- OOS expectancy
- calibration
- drawdown
- robustness
- cost-adjusted performance

without worsening risk beyond limits.

## Model rollback

Keep previous production model/version available.

Rollback triggers:
- severe drift
- calibration collapse
- drawdown breach
- anomalous prediction distribution
- live/replay divergence
- data pipeline anomaly

Rollback is a deployment operation, not an AI decision.

## Explainability

For every model-driven trade score, log:
- model version
- top contributing features
- regime
- calibrated probability / expected value
- uncertainty/confidence
- feature timestamp
- input data hash

Explainability is for audit/debugging, not as proof the model is correct.

## Uncertainty

ASTRA should explicitly represent uncertainty.

Methods:
- probability calibration
- ensembles
- prediction intervals where suitable
- bootstrap confidence
- Bayesian/posterior approaches where justified

Low-confidence predictions get less or no risk.

## Cost-aware ML objective

Do not optimize classification accuracy alone.

Prefer objectives linked to:
- net expectancy
- turnover
- slippage
- drawdown
- calibration
- risk-adjusted return

A highly accurate model can still lose money if gains/losses are asymmetric.

## Class imbalance

For rare events:
- report precision/recall
- PR-AUC
- calibrated probabilities
- economic value

Do not celebrate accuracy on highly imbalanced labels.

## LLM role

LLMs can help:
- summarize research
- generate hypotheses
- inspect logs
- classify qualitative event context
- explain model behavior

LLMs should not be the sole source of:
- live price predictions
- order size
- stop placement
- kill-switch control

Any LLM-derived signal must pass deterministic feature/risk/execution gates.

## Adversarial and failure considerations

Test:
- missing features
- stale features
- extreme values
- malformed input
- model service timeout
- model output NaN/inf
- distribution shift

Failure policy:
NO MODEL OUTPUT = NO MODEL-DEPENDENT TRADE

Do not fall back to an unvalidated guess.

## Reproducibility

Each model artifact records:
- training data version/hash
- feature set version
- code commit
- hyperparameters
- random seed
- training window
- validation windows
- metrics
- calibration artifact
- dependency versions

## Initial ASTRA AI plan

Phase 1:
- deterministic strategy/risk baselines
- no ML needed for execution

Phase 2:
- regime classifier
- signal-quality ranker
- slippage/liquidity estimator

Phase 3:
- ensemble/meta-model
- drift monitor
- champion/challenger deployment

Deep learning or reinforcement learning should remain research-only until simpler methods clearly plateau and data quality is sufficient.

## Reinforcement learning policy

RL should not be used as the first live decision engine.

Reasons:
- simulator mismatch
- reward hacking
- unstable policies
- difficult attribution
- high sample demand

If researched:
- offline only
- conservative action space
- strict risk shield outside agent
- shadow evaluation before any capital

## Core principle

AI may recommend.
Risk decides.
Execution verifies.
Deployment governs.

from __future__ import annotations

from dataclasses import dataclass
from math import erf, exp, log, sqrt

@dataclass(frozen=True)
class MultipleTestingResult:
    observed_sharpe: float
    trials: int
    adjusted_threshold: float
    deflated_sharpe_z: float
    confidence: float

def _normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + erf(x / sqrt(2.0)))

def deflated_sharpe(
    *,
    observed_sharpe: float,
    trials: int,
    sample_size: int,
    skew: float = 0.0,
    kurtosis: float = 3.0,
) -> MultipleTestingResult:
    if trials < 1 or sample_size < 2:
        raise ValueError("trials>=1 and sample_size>=2 required")

    # Conservative multiple-testing threshold approximation.
    threshold = sqrt(max(0.0, 2.0 * log(max(1, trials)))) / sqrt(sample_size)

    denom_sq = max(
        1e-12,
        (1.0 - skew * observed_sharpe + ((kurtosis - 1.0) / 4.0) * observed_sharpe**2)
        / max(1, sample_size - 1),
    )
    z = (observed_sharpe - threshold) / sqrt(denom_sq)
    return MultipleTestingResult(
        observed_sharpe=observed_sharpe,
        trials=trials,
        adjusted_threshold=threshold,
        deflated_sharpe_z=z,
        confidence=_normal_cdf(z),
    )

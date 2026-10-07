from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class ExpiryRegime:
    is_expiry_day: bool
    days_to_expiry: int
    gamma_sensitive: bool

def classify_expiry_regime(*, days_to_expiry: int, abs_gamma: float, gamma_threshold: float) -> ExpiryRegime:
    return ExpiryRegime(
        is_expiry_day=days_to_expiry==0,
        days_to_expiry=days_to_expiry,
        gamma_sensitive=abs_gamma>=gamma_threshold,
    )

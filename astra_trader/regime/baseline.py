from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

class Regime(str, Enum):
    TREND_LOW_VOL="TREND_LOW_VOL"
    TREND_HIGH_VOL="TREND_HIGH_VOL"
    RANGE_LOW_VOL="RANGE_LOW_VOL"
    RANGE_HIGH_VOL="RANGE_HIGH_VOL"

@dataclass(frozen=True)
class RegimeInputs:
    trend_strength: float
    realized_vol: float
    trend_threshold: float
    vol_threshold: float

def classify_regime(x: RegimeInputs) -> Regime:
    trend=abs(x.trend_strength) >= x.trend_threshold
    high_vol=x.realized_vol >= x.vol_threshold
    if trend and high_vol:
        return Regime.TREND_HIGH_VOL
    if trend:
        return Regime.TREND_LOW_VOL
    if high_vol:
        return Regime.RANGE_HIGH_VOL
    return Regime.RANGE_LOW_VOL

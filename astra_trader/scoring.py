from dataclasses import dataclass

@dataclass(frozen=True)
class SignalInputs:
    trend: float
    volume: float
    vwap_alignment: float
    oi_alignment: float
    pcr_alignment: float
    iv_quality: float
    greek_quality: float
    liquidity: float

def _clamp(value: float) -> float:
    return max(0.0, min(100.0, value))

def score_signal(x: SignalInputs) -> float:
    weights = {
        "trend": 0.20,
        "volume": 0.15,
        "vwap_alignment": 0.15,
        "oi_alignment": 0.15,
        "pcr_alignment": 0.10,
        "iv_quality": 0.10,
        "greek_quality": 0.10,
        "liquidity": 0.05,
    }
    total = sum(_clamp(getattr(x, key)) * weight for key, weight in weights.items())
    return round(total, 2)

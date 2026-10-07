from __future__ import annotations

def drawdown_multiplier(drawdown_pct: float) -> float:
    d=abs(drawdown_pct)
    if d < 3:
        return 1.0
    if d < 5:
        return 0.75
    if d < 8:
        return 0.5
    return 0.0

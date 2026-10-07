from __future__ import annotations

def volatility_expansion(current_range: float, historical_ranges: list[float], multiplier: float=1.5) -> bool:
    if not historical_ranges:
        return False
    baseline=sum(historical_ranges)/len(historical_ranges)
    return baseline>0 and current_range >= baseline*multiplier

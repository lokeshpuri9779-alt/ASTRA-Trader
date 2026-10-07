from __future__ import annotations

def pct_change(values: list[float]) -> float:
    if len(values) < 2 or values[0] == 0:
        return 0.0
    return values[-1] / values[0] - 1.0

def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0

def stdev(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    m=mean(values)
    return (sum((x-m)**2 for x in values)/(len(values)-1))**0.5

def zscore(value: float, history: list[float]) -> float:
    s=stdev(history)
    return (value-mean(history))/s if s>0 else 0.0

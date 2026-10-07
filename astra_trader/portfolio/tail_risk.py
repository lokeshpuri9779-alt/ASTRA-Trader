from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class TailRisk:
    var: float
    cvar: float

def historical_var_cvar(pnls: list[float], alpha: float = 0.95) -> TailRisk:
    if not pnls:
        raise ValueError("Need PnL observations.")
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1.")
    ordered=sorted(pnls)
    idx=max(0, min(len(ordered)-1, int((1-alpha)*len(ordered))))
    var=ordered[idx]
    tail=ordered[:idx+1]
    cvar=sum(tail)/len(tail)
    return TailRisk(var=var,cvar=cvar)

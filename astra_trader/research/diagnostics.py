from __future__ import annotations

from dataclasses import dataclass
from math import sqrt

@dataclass(frozen=True)
class Diagnostics:
    mean_return: float
    volatility: float
    sharpe: float
    max_drawdown: float
    profit_factor: float

def summarize(returns: list[float]) -> Diagnostics:
    if not returns:
        raise ValueError("Need returns.")
    mean=sum(returns)/len(returns)
    var=sum((x-mean)**2 for x in returns)/max(1,len(returns)-1)
    vol=sqrt(var)
    sharpe=mean/vol*sqrt(len(returns)) if vol>0 else 0.0
    equity=[]
    total=0.0
    for r in returns:
        total += r
        equity.append(total)
    peak=equity[0]
    max_dd=0.0
    for x in equity:
        peak=max(peak,x)
        max_dd=min(max_dd,x-peak)
    gains=sum(x for x in returns if x>0)
    losses=-sum(x for x in returns if x<0)
    pf=gains/losses if losses>0 else float("inf")
    return Diagnostics(mean,vol,sharpe,max_dd,pf)

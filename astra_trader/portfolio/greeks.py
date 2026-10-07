from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class Greeks:
    delta: float=0.0
    gamma: float=0.0
    theta: float=0.0
    vega: float=0.0

def aggregate_greeks(legs: list[tuple[int,Greeks]]) -> Greeks:
    d=g=t=v=0.0
    for qty,x in legs:
        d += qty*x.delta
        g += qty*x.gamma
        t += qty*x.theta
        v += qty*x.vega
    return Greeks(d,g,t,v)

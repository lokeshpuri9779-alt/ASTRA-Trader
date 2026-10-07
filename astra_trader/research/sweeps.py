from __future__ import annotations

from itertools import product

def parameter_grid(space: dict[str, list]) -> list[dict]:
    keys=list(space.keys())
    if not keys:
        return [{}]
    return [dict(zip(keys,vals)) for vals in product(*(space[k] for k in keys))]

def robustness_neighbors(base: dict[str,float], pct: float=0.1) -> list[dict]:
    out=[dict(base)]
    for k,v in base.items():
        if isinstance(v,(int,float)):
            for m in (1-pct,1+pct):
                x=dict(base)
                x[k]=type(v)(v*m) if isinstance(v,int) else v*m
                out.append(x)
    return out

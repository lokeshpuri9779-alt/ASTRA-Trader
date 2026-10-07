from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class Candidate:
    name: str
    score: float
    risk_rupees: float
    cluster: str

@dataclass(frozen=True)
class Allocation:
    name: str
    allocated_risk: float

def allocate_risk(candidates: list[Candidate], *, total_risk_budget: float, max_cluster_fraction: float=0.5) -> list[Allocation]:
    if total_risk_budget <= 0:
        return []
    ordered=sorted(candidates,key=lambda c:c.score,reverse=True)
    cluster_used={}
    remaining=total_risk_budget
    out=[]
    for c in ordered:
        if remaining <= 0:
            break
        cluster_cap=total_risk_budget*max_cluster_fraction
        used=cluster_used.get(c.cluster,0.0)
        cluster_remaining=max(0.0,cluster_cap-used)
        amount=min(c.risk_rupees,cluster_remaining,remaining)
        if amount <= 0:
            continue
        out.append(Allocation(c.name,amount))
        cluster_used[c.cluster]=used+amount
        remaining -= amount
    return out

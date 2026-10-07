from __future__ import annotations

import random
from dataclasses import dataclass

@dataclass(frozen=True)
class MonteCarloSummary:
    median_final_pnl: float
    worst_final_pnl: float
    best_final_pnl: float
    median_max_drawdown: float

def _max_drawdown(path: list[float]) -> float:
    peak=path[0] if path else 0.0
    worst=0.0
    for x in path:
        peak=max(peak,x)
        worst=min(worst,x-peak)
    return worst

def resample_trade_pnls(trade_pnls: list[float], *, runs: int = 1000, seed: int = 1) -> MonteCarloSummary:
    if not trade_pnls:
        raise ValueError("Need trades.")
    rng=random.Random(seed)
    finals=[]
    dds=[]
    for _ in range(runs):
        sample=[rng.choice(trade_pnls) for _ in trade_pnls]
        equity=[]
        total=0.0
        for pnl in sample:
            total += pnl
            equity.append(total)
        finals.append(total)
        dds.append(_max_drawdown(equity))
    finals.sort()
    dds.sort()
    mid=len(finals)//2
    return MonteCarloSummary(finals[mid],finals[0],finals[-1],dds[len(dds)//2])

from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class Divergence:
    fill_price_bps: float
    quantity_difference: int
    pnl_difference: float

def compare_execution(
    *,
    replay_price: float,
    observed_shadow_price: float,
    replay_qty: int,
    shadow_qty: int,
    replay_pnl: float,
    shadow_pnl: float,
) -> Divergence:
    midpoint=max(1e-12,(abs(replay_price)+abs(observed_shadow_price))/2)
    bps=(observed_shadow_price-replay_price)/midpoint*10000
    return Divergence(
        fill_price_bps=bps,
        quantity_difference=shadow_qty-replay_qty,
        pnl_difference=shadow_pnl-replay_pnl,
    )

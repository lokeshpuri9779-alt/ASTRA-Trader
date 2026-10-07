from __future__ import annotations

def liquidity_position_cap(
    *,
    average_daily_volume: float,
    participation_rate: float,
    lot_size: int = 1,
) -> int:
    if average_daily_volume <= 0 or participation_rate <= 0 or lot_size <= 0:
        return 0
    raw=int(average_daily_volume*participation_rate)
    return (raw//lot_size)*lot_size

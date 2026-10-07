from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class StopExecution:
    triggered: bool
    fill_price: float | None

def stop_market_fill(*, side: str, stop_price: float, next_open: float, next_low: float, next_high: float) -> StopExecution:
    """Conservative stop-market handling for bar replay.

    Long-position exit uses SELL stop: if next open gaps below stop, fill at next open.
    Short-position exit uses BUY stop: if next open gaps above stop, fill at next open.
    """
    side = side.upper()
    if side == "SELL":
        if next_open <= stop_price:
            return StopExecution(True, next_open)
        if next_low <= stop_price:
            return StopExecution(True, stop_price)
        return StopExecution(False, None)

    if side == "BUY":
        if next_open >= stop_price:
            return StopExecution(True, next_open)
        if next_high >= stop_price:
            return StopExecution(True, stop_price)
        return StopExecution(False, None)

    raise ValueError("side must be BUY or SELL")

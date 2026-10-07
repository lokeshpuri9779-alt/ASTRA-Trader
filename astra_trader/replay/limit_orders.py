from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class LimitFill:
    filled: bool
    price: float | None

def limit_fill_bar(*, side: str, limit_price: float, bar_open: float, bar_low: float, bar_high: float) -> LimitFill:
    side = side.upper()
    if side == "BUY":
        if bar_open <= limit_price:
            return LimitFill(True, bar_open)
        if bar_low <= limit_price:
            return LimitFill(True, limit_price)
        return LimitFill(False, None)
    if side == "SELL":
        if bar_open >= limit_price:
            return LimitFill(True, bar_open)
        if bar_high >= limit_price:
            return LimitFill(True, limit_price)
        return LimitFill(False, None)
    raise ValueError("side must be BUY or SELL")

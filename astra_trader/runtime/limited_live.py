from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class LimitedLiveLimits:
    max_notional_per_order: float
    max_daily_notional: float
    max_open_orders: int
    max_orders_per_minute: int

@dataclass(frozen=True)
class LimitedLiveDecision:
    allowed: bool
    reason: str

def check_limited_live(
    *,
    order_notional: float,
    daily_notional: float,
    open_orders: int,
    orders_last_minute: int,
    limits: LimitedLiveLimits,
) -> LimitedLiveDecision:
    if order_notional > limits.max_notional_per_order:
        return LimitedLiveDecision(False, "ORDER_NOTIONAL_LIMIT")
    if daily_notional + order_notional > limits.max_daily_notional:
        return LimitedLiveDecision(False, "DAILY_NOTIONAL_LIMIT")
    if open_orders >= limits.max_open_orders:
        return LimitedLiveDecision(False, "OPEN_ORDER_LIMIT")
    if orders_last_minute >= limits.max_orders_per_minute:
        return LimitedLiveDecision(False, "RATE_LIMIT")
    return LimitedLiveDecision(True, "OK")

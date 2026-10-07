from __future__ import annotations

from astra_trader.execution.interfaces import OrderStatus

UPSTOX_STATUS_MAP = {
    "created": OrderStatus.CREATED,
    "submitted": OrderStatus.SUBMITTED,
    "acknowledged": OrderStatus.ACKNOWLEDGED,
    "open": OrderStatus.ACKNOWLEDGED,
    "partially_filled": OrderStatus.PARTIALLY_FILLED,
    "filled": OrderStatus.FILLED,
    "complete": OrderStatus.FILLED,
    "rejected": OrderStatus.REJECTED,
    "cancelled": OrderStatus.CANCELLED,
    "canceled": OrderStatus.CANCELLED,
    "unknown_submission": OrderStatus.UNKNOWN_SUBMISSION,
}

def map_upstox_order_status(raw_status: str) -> OrderStatus:
    key=raw_status.strip().lower().replace(" ","_").replace("-","_")
    return UPSTOX_STATUS_MAP.get(key,OrderStatus.UNKNOWN_SUBMISSION)

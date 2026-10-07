from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

class SimOrderState(str, Enum):
    CREATED = "CREATED"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"

@dataclass
class SimOrder:
    client_order_id: str
    symbol: str
    side: str
    quantity: int
    order_type: str
    limit_price: float | None = None
    trigger_price: float | None = None
    filled_quantity: int = 0
    average_fill_price: float = 0.0
    state: SimOrderState = SimOrderState.CREATED
    reject_reason: str | None = None

    @property
    def remaining(self) -> int:
        return max(0, self.quantity - self.filled_quantity)

    def acknowledge(self) -> None:
        if self.state is not SimOrderState.CREATED:
            raise ValueError("Only CREATED orders can be acknowledged.")
        self.state = SimOrderState.ACKNOWLEDGED

    def reject(self, reason: str) -> None:
        if self.state in {SimOrderState.FILLED, SimOrderState.CANCELLED, SimOrderState.EXPIRED}:
            raise ValueError("Terminal order cannot be rejected.")
        self.reject_reason = reason
        self.state = SimOrderState.REJECTED

    def apply_fill(self, quantity: int, price: float) -> None:
        if quantity <= 0 or quantity > self.remaining:
            raise ValueError("Invalid fill quantity.")
        prev_notional = self.average_fill_price * self.filled_quantity
        self.filled_quantity += quantity
        self.average_fill_price = (prev_notional + price * quantity) / self.filled_quantity
        self.state = SimOrderState.FILLED if self.remaining == 0 else SimOrderState.PARTIALLY_FILLED

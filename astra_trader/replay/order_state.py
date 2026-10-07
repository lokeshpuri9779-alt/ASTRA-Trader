from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

class OrderState(str, Enum):
    CREATED = "CREATED"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"

_ALLOWED = {
    OrderState.CREATED: {OrderState.ACKNOWLEDGED, OrderState.REJECTED, OrderState.CANCELLED},
    OrderState.ACKNOWLEDGED: {OrderState.PARTIALLY_FILLED, OrderState.FILLED, OrderState.REJECTED, OrderState.CANCELLED, OrderState.EXPIRED},
    OrderState.PARTIALLY_FILLED: {OrderState.PARTIALLY_FILLED, OrderState.FILLED, OrderState.CANCELLED, OrderState.EXPIRED},
    OrderState.FILLED: set(),
    OrderState.REJECTED: set(),
    OrderState.CANCELLED: set(),
    OrderState.EXPIRED: set(),
}

@dataclass
class SimulatedOrder:
    client_order_id: str
    symbol: str
    side: str
    quantity: int
    state: OrderState = OrderState.CREATED
    filled_quantity: int = 0
    average_fill_price: float = 0.0
    history: list[tuple[str, str]] = field(default_factory=list)

    def transition(self, new_state: OrderState, reason: str = "") -> None:
        if new_state not in _ALLOWED[self.state]:
            raise ValueError(f"Invalid order transition {self.state} -> {new_state}")
        self.history.append((new_state.value, reason))
        self.state = new_state

    def apply_fill(self, quantity: int, price: float) -> None:
        if quantity <= 0 or quantity > self.quantity - self.filled_quantity:
            raise ValueError("Invalid fill quantity.")
        previous_notional = self.average_fill_price * self.filled_quantity
        self.filled_quantity += quantity
        self.average_fill_price = (previous_notional + quantity * price) / self.filled_quantity
        target_state = OrderState.FILLED if self.filled_quantity == self.quantity else OrderState.PARTIALLY_FILLED
        self.transition(target_state, f"fill {quantity}@{price}")

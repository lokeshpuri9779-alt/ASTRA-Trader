from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
import uuid

class OrderStatus(str, Enum):
    CREATED = "CREATED"
    SUBMITTED = "SUBMITTED"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"
    UNKNOWN_SUBMISSION = "UNKNOWN_SUBMISSION"

@dataclass(frozen=True)
class OrderIntent:
    symbol: str
    side: str
    quantity: int
    order_type: str
    limit_price: float | None = None
    trigger_price: float | None = None
    client_order_id: str = ""

    def with_id(self) -> "OrderIntent":
        if self.client_order_id:
            return self
        return OrderIntent(
            symbol=self.symbol,
            side=self.side,
            quantity=self.quantity,
            order_type=self.order_type,
            limit_price=self.limit_price,
            trigger_price=self.trigger_price,
            client_order_id=str(uuid.uuid4()),
        )

class ExecutionGateway(ABC):
    @abstractmethod
    def submit(self, intent: OrderIntent) -> OrderStatus:
        raise NotImplementedError

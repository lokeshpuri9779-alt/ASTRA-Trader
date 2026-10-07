from __future__ import annotations

from dataclasses import dataclass, field

from astra_trader.replay.order_state import OrderState, SimulatedOrder

@dataclass
class SimulatedOrderBook:
    orders: dict[str, SimulatedOrder] = field(default_factory=dict)

    def add(self, order: SimulatedOrder) -> None:
        if order.client_order_id in self.orders:
            raise ValueError("Duplicate client_order_id")
        self.orders[order.client_order_id] = order

    def open_orders(self) -> list[SimulatedOrder]:
        terminal={OrderState.FILLED,OrderState.REJECTED,OrderState.CANCELLED,OrderState.EXPIRED}
        return [o for o in self.orders.values() if o.state not in terminal]

from __future__ import annotations

from dataclasses import dataclass, field

from astra_trader.execution.upstox_sandbox import SandboxOrder, SandboxOrderResult

@dataclass
class DeterministicUpstoxSandbox:
    """Pure local simulator for Upstox sandbox lifecycle tests.

    No network calls, no credentials, no live broker interaction.
    """
    orders: dict[str, SandboxOrderResult] = field(default_factory=dict)
    client_ids: set[str] = field(default_factory=set)
    sequence: int = 0

    def submit(self, order: SandboxOrder) -> SandboxOrderResult:
        if not order.client_order_id:
            return SandboxOrderResult(False,None,"REJECTED","MISSING_CLIENT_ORDER_ID")
        if order.client_order_id in self.client_ids:
            return SandboxOrderResult(False,None,"REJECTED","DUPLICATE_CLIENT_ORDER_ID")
        if order.quantity <= 0:
            return SandboxOrderResult(False,None,"REJECTED","INVALID_QUANTITY")

        self.sequence += 1
        broker_order_id=f"SIM-{self.sequence:06d}"
        result=SandboxOrderResult(True,broker_order_id,"ACKNOWLEDGED","SIMULATED")
        self.client_ids.add(order.client_order_id)
        self.orders[broker_order_id]=result
        return result

    def get_order(self, broker_order_id: str) -> SandboxOrderResult:
        return self.orders.get(
            broker_order_id,
            SandboxOrderResult(False,None,"UNKNOWN","ORDER_NOT_FOUND"),
        )

    def cancel(self, broker_order_id: str) -> SandboxOrderResult:
        current=self.orders.get(broker_order_id)
        if current is None:
            return SandboxOrderResult(False,None,"UNKNOWN","ORDER_NOT_FOUND")
        cancelled=SandboxOrderResult(True,broker_order_id,"CANCELLED","SIMULATED")
        self.orders[broker_order_id]=cancelled
        return cancelled

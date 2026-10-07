from __future__ import annotations

from dataclasses import dataclass, field
import hashlib

from astra_trader.execution.upstox_sandbox import SandboxOrder

def deterministic_client_order_id(order: SandboxOrder) -> str:
    raw="|".join([
        order.symbol,
        order.side.upper(),
        str(order.quantity),
        order.order_type.upper(),
    ])
    return "ASTRA-" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:20]

@dataclass
class SandboxIdempotencyRegistry:
    seen: set[str] = field(default_factory=set)

    def accept(self, client_order_id: str) -> bool:
        if not client_order_id or client_order_id in self.seen:
            return False
        self.seen.add(client_order_id)
        return True

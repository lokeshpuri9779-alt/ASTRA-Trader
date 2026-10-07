from astra_trader.execution.interfaces import OrderStatus
from astra_trader.execution.sandbox_idempotency import SandboxIdempotencyRegistry
from astra_trader.execution.upstox_lifecycle import map_upstox_order_status
from astra_trader.execution.upstox_reconcile import UpstoxPositionRow, reconcile_upstox_positions
from astra_trader.execution.upstox_sandbox import SandboxOrder
from astra_trader.execution.upstox_sandbox_sim import DeterministicUpstoxSandbox
from astra_trader.runtime.static_ip import validate_static_ips

def test_sandbox_duplicate_protection():
    sim=DeterministicUpstoxSandbox()
    order=SandboxOrder("NSE_EQ|ABC","BUY",1,"MARKET","abc")
    first=sim.submit(order)
    second=sim.submit(order)
    assert first.accepted
    assert not second.accepted
    assert second.message=="DUPLICATE_CLIENT_ORDER_ID"

def test_lifecycle_mapper():
    assert map_upstox_order_status("complete") is OrderStatus.FILLED
    assert map_upstox_order_status("mystery") is OrderStatus.UNKNOWN_SUBMISSION

def test_upstox_reconciliation_mapper():
    r=reconcile_upstox_positions({"NSE_EQ|ABC":2},[UpstoxPositionRow("NSE_EQ|ABC",2)])
    assert r.ok

def test_static_ip_validator():
    assert validate_static_ips("8.8.8.8","1.1.1.1").ok
    assert not validate_static_ips("192.168.1.10").ok

def test_sandbox_idempotency_registry():
    reg=SandboxIdempotencyRegistry()
    assert reg.accept("x")
    assert not reg.accept("x")

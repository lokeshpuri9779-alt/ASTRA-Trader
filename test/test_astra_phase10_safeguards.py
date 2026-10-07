import pytest

from astra_trader.execution.idempotency import IdempotencyStore
from astra_trader.execution.interfaces import OrderIntent, OrderStatus
from astra_trader.execution.kill_switch import KillSwitch
from astra_trader.execution.reconciliation import PositionSnapshot, reconcile_startup
from astra_trader.execution.recovery import RecoveryAction, recovery_plan
from astra_trader.runtime.limited_live import LimitedLiveLimits, check_limited_live
from astra_trader.runtime.promotion_policy import (
    ProductionPromotionEvidence,
    evaluate_production_promotion,
)

def test_idempotency_store_blocks_duplicate_client_id():
    i=OrderIntent("NIFTY","BUY",1,"MARKET",client_order_id="abc")
    s=IdempotencyStore()
    assert s.reserve(i)
    assert not s.reserve(i)
    s.update("abc",OrderStatus.ACKNOWLEDGED)
    assert s.statuses["abc"] is OrderStatus.ACKNOWLEDGED

def test_startup_reconciliation_detects_mismatch():
    r=reconcile_startup({"NIFTY":1},[PositionSnapshot("NIFTY",2)])
    assert not r.ok and r.mismatches==("NIFTY",)

def test_unknown_submission_blocks_new_risk():
    p=recovery_plan(broker_supports_client_id_query=True,age_seconds=5)
    assert RecoveryAction.BLOCK_NEW_RISK in p.actions
    assert RecoveryAction.QUERY_BY_CLIENT_ID in p.actions

def test_kill_switch_blocks_submission():
    k=KillSwitch()
    k.engage("TEST")
    with pytest.raises(RuntimeError):
        k.assert_can_submit()

def test_limited_live_caps():
    limits=LimitedLiveLimits(10000,50000,3,5)
    assert check_limited_live(
        order_notional=5000,daily_notional=10000,open_orders=1,orders_last_minute=1,limits=limits
    ).allowed
    assert not check_limited_live(
        order_notional=15000,daily_notional=10000,open_orders=1,orders_last_minute=1,limits=limits
    ).allowed

def test_production_promotion_requires_external_and_user_gates():
    e=ProductionPromotionEvidence(
        integrated_validation_passed=True,
        broker_reconciliation_passed=False,
        kill_switch_tested=True,
        unknown_submission_recovery_tested=True,
        static_ip_verified=False,
        credentials_loaded_securely=False,
        limited_live_completed=False,
        zero_unresolved_incidents=True,
        explicit_user_authorization=False,
    )
    d=evaluate_production_promotion(e)
    assert not d.allowed
    assert "USER_AUTHORIZATION" in d.missing

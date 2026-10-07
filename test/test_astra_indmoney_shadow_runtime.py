from datetime import datetime, timezone

from astra_trader.integrations.indmoney import IndMoneyMarketContext, IndMoneyPosition
from astra_trader.integrations.indmoney_snapshot import build_snapshot
from astra_trader.paper.shadow_runtime import IndMoneyShadowRuntime

def test_read_only_snapshot_can_drive_shadow_monitoring_without_orders():
    snapshot=build_snapshot(
        captured_at=datetime.now(timezone.utc),
        positions=[IndMoneyPosition("ABC",10,average_price=100,current_price=105)],
        market_context=[IndMoneyMarketContext("ABC",last_price=106)],
    )
    runtime=IndMoneyShadowRuntime()
    result=runtime.assess(snapshot)
    assert len(result.assessments)==1
    assert result.assessments[0].action=="MONITOR"
    assert result.assessments[0].reference_price==106
    assert result.hypothetical_orders==0

def test_hypothetical_intent_never_calls_external_execution():
    runtime=IndMoneyShadowRuntime()
    runtime.record_hypothetical(
        symbol="ABC",side="BUY",quantity=1,reference_price=100,
    )
    assert len(runtime.gateway.intents)==1

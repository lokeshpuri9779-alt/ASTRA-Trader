from datetime import datetime,timedelta

from astra_trader.observability.degradation import strategy_health
from astra_trader.observability.drift import population_stability_index
from astra_trader.observability.heartbeat import Heartbeat,is_stale
from astra_trader.observability.reconciliation import reconcile_positions
from astra_trader.observability.watchdog import watchdog_decision

def test_health_monitors():
    now=datetime(2026,1,1,12)
    h=Heartbeat("data",now-timedelta(seconds=20))
    assert is_stale(h,now=now,max_age=timedelta(seconds=10))
    r=reconcile_positions({"A":1},{"A":2})
    assert not r.matched
    assert strategy_health(drawdown_pct=6,expected_drawdown_limit=5,expectancy=1).state=="DISABLED"
    assert population_stability_index([50,50],[80,20])>0
    w=watchdog_decision(stale_data=True,reconciliation_ok=True,component_healthy=True)
    assert w.block_new_risk

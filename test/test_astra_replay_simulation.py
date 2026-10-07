from datetime import datetime

from astra_trader.replay.expiry import settle_option
from astra_trader.replay.latency import LatencyModel
from astra_trader.replay.limit_orders import limit_fill_bar
from astra_trader.replay.stress import Scenario, linear_delta_stress

def test_limit_buy_gap_better_price():
    result = limit_fill_bar(side="BUY", limit_price=100, bar_open=98, bar_low=97, bar_high=105)
    assert result.filled and result.price == 98

def test_latency_model():
    t = datetime(2026,1,1)
    model = LatencyModel(10,20,30,40)
    assert (model.order_eligible_at(t)-t).total_seconds() == 0.1

def test_option_settlement():
    result = settle_option(option_type="CE", strike=100, settlement_underlying=110)
    assert result.intrinsic_value == 10
    assert not result.expires_worthless

def test_delta_stress():
    r = linear_delta_stress(position_delta_rupees=100000, scenario=Scenario("down2", -2))
    assert r.pnl == -2000

from astra_trader.portfolio.allocator import Candidate, allocate_risk
from astra_trader.portfolio.drawdown import drawdown_multiplier
from astra_trader.portfolio.exposure import aggregate_exposure
from astra_trader.portfolio.greeks import Greeks, aggregate_greeks
from astra_trader.portfolio.sizing import inverse_vol_weights, volatility_adjusted_size

def test_exposure_and_sizing():
    x=aggregate_exposure([
        {"symbol":"A","underlying":"NIFTY","side":"BUY","notional":100},
        {"symbol":"B","underlying":"NIFTY","side":"SELL","notional":40},
    ])
    assert x.gross==140 and x.net==60 and x.by_underlying["NIFTY"]==60
    assert volatility_adjusted_size(base_risk_rupees=1000,stop_distance=10,volatility_scale=2)==50
    w=inverse_vol_weights({"a":1,"b":2})
    assert round(w["a"],6)==round(2/3,6)

def test_drawdown_and_greeks():
    assert drawdown_multiplier(4)==0.75
    g=aggregate_greeks([(2,Greeks(delta=.5,vega=1)),(-1,Greeks(delta=.2,vega=.5))])
    assert round(g.delta,6)==0.8 and round(g.vega,6)==1.5

def test_allocator_cluster_cap():
    out=allocate_risk([
        Candidate("a",90,600,"index"),
        Candidate("b",80,600,"index"),
        Candidate("c",70,600,"other"),
    ],total_risk_budget=1000,max_cluster_fraction=.5)
    assert sum(x.allocated_risk for x in out)<=1000
    assert sum(x.allocated_risk for x in out if x.name in {"a","b"})<=500

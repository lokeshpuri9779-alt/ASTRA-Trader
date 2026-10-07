from datetime import datetime

from astra_trader.core.events import Event, EventType
from astra_trader.features.derivatives import futures_basis_pct, put_call_oi_ratio
from astra_trader.regime.baseline import Regime, RegimeInputs, classify_regime
from astra_trader.strategies.mean_reversion import ZScoreMeanReversionStrategy
from astra_trader.strategies.trend import TrendBreakoutStrategy

def ev(close):
    t=datetime(2026,1,1)
    return Event(EventType.MARKET_DATA,t,t,{"instrument_id":"NIFTY","close":close})

def test_regime_classifier():
    assert classify_regime(RegimeInputs(2,1,1,2)) is Regime.TREND_LOW_VOL
    assert classify_regime(RegimeInputs(0.5,3,1,2)) is Regime.RANGE_HIGH_VOL

def test_derivative_context():
    assert round(futures_basis_pct(futures_price=101,spot_price=100),6)==1
    assert put_call_oi_ratio(put_oi=200,call_oi=100)==2

def test_trend_baseline_emits_after_history():
    s=TrendBreakoutStrategy(lookback=3,threshold=0)
    assert s.on_event(ev(100))==[]
    assert s.on_event(ev(101))==[]
    assert s.on_event(ev(102))==[]
    out=s.on_event(ev(103))
    assert out and out[0].side=="BUY"

def test_mean_reversion_runs():
    s=ZScoreMeanReversionStrategy(lookback=3,entry_z=0.5)
    s.on_event(ev(100)); s.on_event(ev(100))
    out=s.on_event(ev(90))
    assert out

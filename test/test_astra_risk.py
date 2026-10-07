from astra_trader.models import RiskState, TradeSignal
from astra_trader.risk import RiskEngine

def test_good_signal_is_allowed():
    engine = RiskEngine()
    signal = TradeSignal(
        symbol="NIFTY_TEST_CE",
        side="BUY",
        entry=100.0,
        stop=90.0,
        target_1=120.0,
        score=85.0,
        spread_pct=0.5,
    )
    state = RiskState(starting_capital=100000.0, current_equity=100000.0)
    decision = engine.evaluate(signal, state)
    assert decision.allowed
    assert decision.quantity > 0
    assert decision.max_loss_rupees <= 500.0

def test_kill_switch_blocks_trade():
    engine = RiskEngine()
    signal = TradeSignal(
        symbol="NIFTY_TEST_CE",
        side="BUY",
        entry=100.0,
        stop=90.0,
        target_1=120.0,
        score=90.0,
    )
    state = RiskState(starting_capital=100000.0, current_equity=100000.0, kill_switch=True)
    decision = engine.evaluate(signal, state)
    assert not decision.allowed
    assert decision.quantity == 0

def test_daily_loss_limit_blocks_trade():
    engine = RiskEngine()
    signal = TradeSignal(
        symbol="NIFTY_TEST_CE",
        side="BUY",
        entry=100.0,
        stop=90.0,
        target_1=120.0,
        score=90.0,
    )
    state = RiskState(
        starting_capital=100000.0,
        current_equity=98000.0,
        realized_pnl_today=-2000.0,
    )
    decision = engine.evaluate(signal, state)
    assert not decision.allowed

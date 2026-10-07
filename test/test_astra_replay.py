from datetime import datetime, timedelta

from astra_trader.core.events import Event, EventType
from astra_trader.models import RiskState, TradeSignal
from astra_trader.portfolio.state import PortfolioState
from astra_trader.replay.engine import ReplayEngine
from astra_trader.strategies.base import Strategy

class OneSignalStrategy(Strategy):
    name = "one-signal"

    def on_event(self, event):
        return [
            TradeSignal(
                symbol="NIFTY_TEST_CE",
                side="BUY",
                entry=100.0,
                stop=90.0,
                target_1=120.0,
                score=85.0,
                spread_pct=0.5,
            )
        ]

def test_replay_orders_events_and_runs_risk():
    now = datetime.utcnow()
    events = [
        Event(EventType.MARKET_DATA, now + timedelta(seconds=1), now + timedelta(seconds=1), {}),
        Event(EventType.MARKET_DATA, now, now, {}),
    ]
    engine = ReplayEngine(OneSignalStrategy())
    result = engine.run(
        events,
        PortfolioState(cash=100000.0, equity=100000.0),
        RiskState(starting_capital=100000.0, current_equity=100000.0),
    )
    assert result.events_processed == 2
    assert result.signals_generated == 2
    assert result.signals_allowed == 2

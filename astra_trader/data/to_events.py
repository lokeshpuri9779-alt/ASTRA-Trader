from __future__ import annotations

from astra_trader.core.events import Event, EventType
from .schema import Bar

def bar_to_event(bar: Bar) -> Event:
    payload = {
        "instrument_id": bar.instrument_id,
        "interval": bar.interval,
        "open": bar.open,
        "high": bar.high,
        "low": bar.low,
        "close": bar.close,
        "volume": bar.volume,
        "open_interest": bar.open_interest,
        "source": bar.source,
    }
    return Event(
        event_type=EventType.MARKET_DATA,
        event_time=bar.timestamp,
        received_at=bar.timestamp,
        payload=payload,
    )

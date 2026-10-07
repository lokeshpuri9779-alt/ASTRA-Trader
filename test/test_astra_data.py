from datetime import datetime
import pytest

from astra_trader.data.schema import Bar, Quote
from astra_trader.data.validation import DataValidationError, validate_bar, validate_quote
from astra_trader.data.to_events import bar_to_event
from astra_trader.core.events import EventType

def test_valid_bar():
    bar = Bar("NIFTY", datetime(2026, 1, 1), "1d", 100, 110, 95, 105, 1000, 500, "test")
    validate_bar(bar)

def test_invalid_bar_rejected():
    bar = Bar("NIFTY", datetime(2026, 1, 1), "1d", 100, 99, 95, 105, 1000, 500, "test")
    with pytest.raises(DataValidationError):
        validate_bar(bar)

def test_crossed_quote_rejected():
    quote = Quote("NIFTY", datetime(2026, 1, 1), bid=101, ask=100)
    with pytest.raises(DataValidationError):
        validate_quote(quote)

def test_bar_becomes_market_event():
    bar = Bar("NIFTY", datetime(2026, 1, 1), "1d", 100, 110, 95, 105, 1000, 500, "test")
    event = bar_to_event(bar)
    assert event.event_type is EventType.MARKET_DATA
    assert event.payload["close"] == 105

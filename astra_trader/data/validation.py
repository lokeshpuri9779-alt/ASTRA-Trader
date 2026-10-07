from __future__ import annotations

from .schema import Bar, Quote

class DataValidationError(ValueError):
    pass

def validate_bar(bar: Bar) -> None:
    if min(bar.open, bar.high, bar.low, bar.close) < 0:
        raise DataValidationError("Negative price in bar.")
    if bar.high < max(bar.open, bar.close, bar.low):
        raise DataValidationError("High is below another OHLC value.")
    if bar.low > min(bar.open, bar.close, bar.high):
        raise DataValidationError("Low is above another OHLC value.")
    if bar.volume < 0:
        raise DataValidationError("Negative volume.")
    if bar.open_interest is not None and bar.open_interest < 0:
        raise DataValidationError("Negative open interest.")

def validate_quote(quote: Quote) -> None:
    for value in (quote.bid, quote.ask, quote.ltp):
        if value is not None and value < 0:
            raise DataValidationError("Negative quote price.")
    if quote.bid is not None and quote.ask is not None and quote.bid > quote.ask:
        raise DataValidationError("Crossed market quote.")

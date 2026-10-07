from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class InstrumentType(str, Enum):
    EQUITY = "EQUITY"
    INDEX = "INDEX"
    FUTURE = "FUTURE"
    OPTION = "OPTION"

@dataclass(frozen=True)
class Instrument:
    instrument_id: str
    exchange: str
    segment: str
    instrument_type: InstrumentType
    symbol: str
    underlying: str | None = None
    expiry: str | None = None
    strike: float | None = None
    option_type: str | None = None
    lot_size: int | None = None
    tick_size: float | None = None

@dataclass(frozen=True)
class Bar:
    instrument_id: str
    timestamp: datetime
    interval: str
    open: float
    high: float
    low: float
    close: float
    volume: float = 0.0
    open_interest: float | None = None
    source: str = ""

@dataclass(frozen=True)
class Quote:
    instrument_id: str
    timestamp: datetime
    bid: float | None = None
    bid_qty: float | None = None
    ask: float | None = None
    ask_qty: float | None = None
    ltp: float | None = None
    volume: float | None = None
    open_interest: float | None = None
    source: str = ""

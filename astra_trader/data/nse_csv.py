from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import csv
from pathlib import Path

from .schema import Bar
from .validation import validate_bar

@dataclass(frozen=True)
class NseCsvColumns:
    timestamp: str
    open: str
    high: str
    low: str
    close: str
    volume: str
    open_interest: str | None = None

class NseBarCsvLoader:
    """Strict loader for normalized/exported NSE-style bar CSV files.

    This adapter is intentionally schema-driven because NSE source file layouts can
    differ by report/product and may change over time. Source-specific parsers should
    map exchange files into this normalized contract.
    """

    def __init__(self, columns: NseCsvColumns, timestamp_format: str):
        self.columns = columns
        self.timestamp_format = timestamp_format

    def load(self, path: str | Path, instrument_id: str, interval: str, source: str) -> list[Bar]:
        rows: list[Bar] = []
        with Path(path).open("r", encoding="utf-8-sig", newline="") as fh:
            reader = csv.DictReader(fh)
            for raw in reader:
                bar = Bar(
                    instrument_id=instrument_id,
                    timestamp=datetime.strptime(raw[self.columns.timestamp], self.timestamp_format),
                    interval=interval,
                    open=float(raw[self.columns.open]),
                    high=float(raw[self.columns.high]),
                    low=float(raw[self.columns.low]),
                    close=float(raw[self.columns.close]),
                    volume=float(raw[self.columns.volume] or 0),
                    open_interest=(
                        float(raw[self.columns.open_interest] or 0)
                        if self.columns.open_interest
                        else None
                    ),
                    source=source,
                )
                validate_bar(bar)
                rows.append(bar)
        rows.sort(key=lambda x: x.timestamp)
        return rows

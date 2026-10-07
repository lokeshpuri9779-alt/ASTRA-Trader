from __future__ import annotations

from datetime import datetime
import csv
from pathlib import Path

from .schema import Bar, Instrument, InstrumentType
from .validation import validate_bar

class NseIndexHistoryLoader:
    """Loader for NSE-style historical index CSV exports."""

    DATE_FIELDS = ("Date", "DATE", "HistoricalDate")
    OPEN_FIELDS = ("Open", "OPEN")
    HIGH_FIELDS = ("High", "HIGH")
    LOW_FIELDS = ("Low", "LOW")
    CLOSE_FIELDS = ("Close", "CLOSE")
    VOLUME_FIELDS = ("Volume", "VOLUME", "Shares Traded")

    @staticmethod
    def _pick(row: dict[str, str], names: tuple[str, ...], required: bool = True) -> str | None:
        for name in names:
            if name in row and row[name] not in (None, ""):
                return row[name]
        if required:
            raise KeyError(f"Missing expected fields: {names}")
        return None

    def load(self, path: str | Path, *, symbol: str, source: str = "NSE_INDEX_HISTORY") -> tuple[Instrument, list[Bar]]:
        instrument = Instrument(
            instrument_id=f"NSE:INDEX:{symbol}",
            exchange="NSE",
            segment="INDEX",
            instrument_type=InstrumentType.INDEX,
            symbol=symbol,
            underlying=symbol,
        )
        bars: list[Bar] = []
        with Path(path).open("r", encoding="utf-8-sig", newline="") as fh:
            for row in csv.DictReader(fh):
                date_raw = self._pick(row, self.DATE_FIELDS)
                parsed = None
                for fmt in ("%d-%b-%Y", "%d-%m-%Y", "%Y-%m-%d", "%d/%m/%Y"):
                    try:
                        parsed = datetime.strptime(date_raw.strip(), fmt)
                        break
                    except ValueError:
                        pass
                if parsed is None:
                    raise ValueError(f"Unsupported NSE index date: {date_raw}")

                close = float(self._pick(row, self.CLOSE_FIELDS).replace(",", ""))
                open_ = float(self._pick(row, self.OPEN_FIELDS).replace(",", ""))
                high = float(self._pick(row, self.HIGH_FIELDS).replace(",", ""))
                low = float(self._pick(row, self.LOW_FIELDS).replace(",", ""))
                volume_raw = self._pick(row, self.VOLUME_FIELDS, required=False)
                volume = float(volume_raw.replace(",", "")) if volume_raw else 0.0

                bar = Bar(
                    instrument_id=instrument.instrument_id,
                    timestamp=parsed,
                    interval="1d",
                    open=open_,
                    high=high,
                    low=low,
                    close=close,
                    volume=volume,
                    source=source,
                )
                validate_bar(bar)
                bars.append(bar)
        bars.sort(key=lambda b: b.timestamp)
        return instrument, bars

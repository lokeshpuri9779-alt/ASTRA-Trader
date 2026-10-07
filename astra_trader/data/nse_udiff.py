from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import csv
from pathlib import Path

from .schema import Bar, Instrument, InstrumentType
from .validation import validate_bar

_REQUIRED = {
    "TradDt",
    "BizDt",
    "Sgmt",
    "Src",
    "FinInstrmTp",
    "FinInstrmId",
    "TckrSymb",
    "OpnPric",
    "HghPric",
    "LwPric",
    "ClsPric",
    "TtlTradgVol",
}

def _clean(value: str | None) -> str:
    return (value or "").strip()

def _float_or_none(value: str | None) -> float | None:
    value = _clean(value)
    if value == "":
        return None
    return float(value)

def _int_or_none(value: str | None) -> int | None:
    value = _clean(value)
    if value == "":
        return None
    return int(float(value))

def _instrument_type(raw: str) -> InstrumentType:
    x = raw.upper()
    if x in {"FUTIDX", "FUTSTK", "FUTIRF", "FUTCUR", "FUTCOM", "FUT"}:
        return InstrumentType.FUTURE
    if x in {"OPTIDX", "OPTSTK", "OPTCUR", "OPTFUT", "OPTCOM", "OPT"}:
        return InstrumentType.OPTION
    if x in {"IDX", "INDEX"}:
        return InstrumentType.INDEX
    return InstrumentType.EQUITY

def _parse_date(value: str | None) -> str | None:
    value = _clean(value)
    if not value:
        return None
    return datetime.fromisoformat(value).date().isoformat()

@dataclass(frozen=True)
class UdiffRecord:
    instrument: Instrument
    bar: Bar
    business_date: str
    settlement_price: float | None
    underlying_price: float | None
    change_in_open_interest: float | None

class NseUdiffBhavcopyLoader:
    """Parser for NSE UDiFF bhavcopy CSV files.

    NSE's UDiFF bhavcopy format uses standard ISO-tag-style column names
    such as TradDt, FinInstrmTp, TckrSymb, XpryDt, StrkPric, OpnPric,
    ClsPric, OpnIntrst and TtlTradgVol.
    """

    def load(self, path: str | Path) -> list[UdiffRecord]:
        records: list[UdiffRecord] = []
        with Path(path).open("r", encoding="utf-8-sig", newline="") as fh:
            reader = csv.DictReader(fh)
            columns = set(reader.fieldnames or [])
            missing = sorted(_REQUIRED - columns)
            if missing:
                raise ValueError(f"UDiFF bhavcopy missing required columns: {missing}")

            for raw in reader:
                trade_date = datetime.fromisoformat(_clean(raw.get("TradDt")))
                fin_type = _clean(raw.get("FinInstrmTp"))
                symbol = _clean(raw.get("TckrSymb"))
                expiry = _parse_date(raw.get("XpryDt"))
                option_type = _clean(raw.get("OptnTp")) or None
                strike = _float_or_none(raw.get("StrkPric"))
                instrument_id = f"NSE:{_clean(raw.get('FinInstrmId'))}"

                instrument = Instrument(
                    instrument_id=instrument_id,
                    exchange="NSE",
                    segment=_clean(raw.get("Sgmt")),
                    instrument_type=_instrument_type(fin_type),
                    symbol=symbol,
                    underlying=symbol,
                    expiry=expiry,
                    strike=strike,
                    option_type=option_type,
                    lot_size=_int_or_none(raw.get("NewBrdLotQty")),
                )

                bar = Bar(
                    instrument_id=instrument_id,
                    timestamp=trade_date,
                    interval="1d",
                    open=float(_clean(raw.get("OpnPric"))),
                    high=float(_clean(raw.get("HghPric"))),
                    low=float(_clean(raw.get("LwPric"))),
                    close=float(_clean(raw.get("ClsPric"))),
                    volume=float(_clean(raw.get("TtlTradgVol")) or 0),
                    open_interest=_float_or_none(raw.get("OpnIntrst")),
                    source="NSE_UDIFF_BHAVCOPY",
                )
                validate_bar(bar)

                records.append(
                    UdiffRecord(
                        instrument=instrument,
                        bar=bar,
                        business_date=_clean(raw.get("BizDt")),
                        settlement_price=_float_or_none(raw.get("SttlmPric")),
                        underlying_price=_float_or_none(raw.get("UndrlygPric")),
                        change_in_open_interest=_float_or_none(raw.get("ChngInOpnIntrst")),
                    )
                )

        records.sort(key=lambda r: (r.bar.timestamp, r.instrument.instrument_id))
        return records

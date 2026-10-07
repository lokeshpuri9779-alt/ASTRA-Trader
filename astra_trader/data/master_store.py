from __future__ import annotations

from dataclasses import asdict
from datetime import date
import json
from pathlib import Path

from .instrument_master import InstrumentMaster, VersionedInstrument
from .schema import Instrument, InstrumentType

def save_instrument_master(master: InstrumentMaster, path: str | Path) -> Path:
    records = []
    for r in master._records:
        item = asdict(r.instrument)
        item["instrument_type"] = r.instrument.instrument_type.value
        records.append({
            "instrument": item,
            "valid_from": r.valid_from.isoformat(),
            "valid_to": r.valid_to.isoformat() if r.valid_to else None,
        })
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(records, sort_keys=True), encoding="utf-8")
    return out

def load_instrument_master(path: str | Path) -> InstrumentMaster:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    records = []
    for row in raw:
        inst = dict(row["instrument"])
        inst["instrument_type"] = InstrumentType(inst["instrument_type"])
        records.append(
            VersionedInstrument(
                instrument=Instrument(**inst),
                valid_from=date.fromisoformat(row["valid_from"]),
                valid_to=date.fromisoformat(row["valid_to"]) if row["valid_to"] else None,
            )
        )
    return InstrumentMaster(records)

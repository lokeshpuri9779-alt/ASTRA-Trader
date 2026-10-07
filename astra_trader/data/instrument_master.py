from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Iterable

from .schema import Instrument

@dataclass(frozen=True)
class VersionedInstrument:
    instrument: Instrument
    valid_from: date
    valid_to: date | None = None

    def is_valid_on(self, day: date) -> bool:
        if day < self.valid_from:
            return False
        return self.valid_to is None or day <= self.valid_to

class InstrumentMaster:
    def __init__(self, records: Iterable[VersionedInstrument] = ()):
        self._records = list(records)

    def add(self, record: VersionedInstrument) -> None:
        self._records.append(record)

    def resolve(self, instrument_id: str, day: date) -> VersionedInstrument:
        matches = [
            r for r in self._records
            if r.instrument.instrument_id == instrument_id and r.is_valid_on(day)
        ]
        if len(matches) != 1:
            raise LookupError(
                f"Expected exactly one instrument version for {instrument_id} on {day}, found {len(matches)}."
            )
        return matches[0]

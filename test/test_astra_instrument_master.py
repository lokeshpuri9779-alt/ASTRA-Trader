from datetime import date
import pytest

from astra_trader.data.instrument_master import InstrumentMaster, VersionedInstrument
from astra_trader.data.schema import Instrument, InstrumentType

def _inst(lot):
    return Instrument(
        instrument_id="NSE:123",
        exchange="NSE",
        segment="FO",
        instrument_type=InstrumentType.OPTION,
        symbol="NIFTY",
        expiry="2026-10-08",
        strike=25000,
        option_type="CE",
        lot_size=lot,
    )

def test_resolves_historical_version():
    master = InstrumentMaster([
        VersionedInstrument(_inst(50), date(2025,1,1), date(2025,12,31)),
        VersionedInstrument(_inst(75), date(2026,1,1), None),
    ])
    assert master.resolve("NSE:123", date(2025,6,1)).instrument.lot_size == 50
    assert master.resolve("NSE:123", date(2026,6,1)).instrument.lot_size == 75

def test_missing_version_fails():
    master = InstrumentMaster()
    with pytest.raises(LookupError):
        master.resolve("NSE:123", date(2026,1,1))

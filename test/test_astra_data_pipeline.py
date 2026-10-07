from datetime import date, datetime
import json
from pathlib import Path
from zipfile import ZipFile

from astra_trader.data.archive import extract_zip_safe
from astra_trader.data.dataset_manifest import DatasetManifest
from astra_trader.data.instrument_master import InstrumentMaster, VersionedInstrument
from astra_trader.data.master_store import load_instrument_master, save_instrument_master
from astra_trader.data.option_snapshot_parser import parse_option_chain_snapshot
from astra_trader.data.quarantine import quarantine_if_invalid
from astra_trader.data.schema import Instrument, InstrumentType

def test_zip_extract_and_master_roundtrip(tmp_path: Path):
    z = tmp_path / "x.zip"
    with ZipFile(z,"w") as f:
        f.writestr("a.txt","ok")
    assert extract_zip_safe(z,tmp_path/"out")[0].read_text() == "ok"

    inst = Instrument("NSE:1","NSE","FO",InstrumentType.OPTION,"NIFTY",expiry="2026-10-08",strike=25000,option_type="CE",lot_size=75)
    master = InstrumentMaster([VersionedInstrument(inst,date(2026,1,1),None)])
    p = save_instrument_master(master,tmp_path/"master.json")
    loaded = load_instrument_master(p)
    assert loaded.resolve("NSE:1",date(2026,5,1)).instrument.lot_size == 75

def test_option_snapshot_and_manifest():
    payload={"records":{"data":[{"strikePrice":25000,"expiryDate":"08-Oct-2026","CE":{"identifier":"C1","lastPrice":100,"openInterest":1000,"bidprice":99,"askPrice":101}}]},"underlyingValue":25010}
    rows=parse_option_chain_snapshot(payload,timestamp=datetime(2026,10,8),underlying_id="NIFTY",source="TEST")
    assert rows[0].spread == 2
    m=DatasetManifest("d1",("a",),("h",),("p1",),"2026-01-01","2026-02-01","m1")
    assert len(m.digest()) == 64

def test_quarantine():
    assert quarantine_if_invalid().accepted
    assert not quarantine_if_invalid(duplicate_count=1).accepted

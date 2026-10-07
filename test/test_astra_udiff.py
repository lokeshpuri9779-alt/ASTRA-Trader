from pathlib import Path

from astra_trader.data.nse_udiff import NseUdiffBhavcopyLoader
from astra_trader.data.schema import InstrumentType
from astra_trader.data.ingestion import build_ingestion_manifest

CSV = """TradDt,BizDt,Sgmt,Src,FinInstrmTp,FinInstrmId,ISIN,TckrSymb,XpryDt,FininstrmActlXpryDt,StrkPric,OptnTp,FinInstrmNm,OpnPric,HghPric,LwPric,ClsPric,LastPric,PrvsClsgPric,UndrlygPric,SttlmPric,OpnIntrst,ChngInOpnIntrst,TtlTradgVol,TtlTrfVal,TtlNbOfTxsExctd,SsnId,NewBrdLotQty,Rmks,Rsvd1,Rsvd2,Rsvd3,Rsvd4
2026-10-06,2026-10-06,FO,NSE,OPTIDX,12345,,NIFTY,2026-10-08,2026-10-08,25000,CE,NIFTY OPTION,100,120,90,110,111,95,25010,110,5000,500,10000,0,100,F1,75,,,,,
"""

def test_udiff_loader(tmp_path: Path):
    p = tmp_path / "bhav.csv"
    p.write_text(CSV, encoding="utf-8")
    records = NseUdiffBhavcopyLoader().load(p)
    assert len(records) == 1
    rec = records[0]
    assert rec.instrument.instrument_type is InstrumentType.OPTION
    assert rec.instrument.symbol == "NIFTY"
    assert rec.instrument.expiry == "2026-10-08"
    assert rec.instrument.strike == 25000.0
    assert rec.instrument.option_type == "CE"
    assert rec.instrument.lot_size == 75
    assert rec.bar.close == 110.0
    assert rec.bar.open_interest == 5000.0
    assert rec.change_in_open_interest == 500.0

def test_ingestion_manifest_hashes_source(tmp_path: Path):
    p = tmp_path / "file.csv"
    p.write_text("abc", encoding="utf-8")
    manifest = build_ingestion_manifest(p, source="NSE", parser_version="1")
    assert len(manifest.file_sha256) == 64
    assert manifest.file_size == 3

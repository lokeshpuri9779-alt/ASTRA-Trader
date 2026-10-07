# ASTRA NSE Ingestion

ASTRA now includes a first source-specific parser for NSE's standardized UDiFF bhavcopy format.

## Supported fields

The parser recognizes the standardized UDiFF bhavcopy tags used by NSE, including:

- TradDt / BizDt
- Sgmt / Src
- FinInstrmTp / FinInstrmId
- TckrSymb
- XpryDt
- StrkPric / OptnTp
- OpnPric / HghPric / LwPric / ClsPric
- UndrlygPric / SttlmPric
- OpnIntrst / ChngInOpnIntrst
- TtlTradgVol
- NewBrdLotQty

## Current scope

The loader is for official downloaded CSV content after any ZIP extraction. It does not attempt to bypass NSE download controls or website protections.

Every source file can receive an ingestion manifest containing:
- source
- filename
- SHA-256
- size
- retrieval time
- parser version

This provides reproducibility and lets later backtests identify the exact raw file version used.

## Safety / correctness

- required columns are validated
- invalid OHLC or negative OI/volume is rejected
- data is normalized into ASTRA Instrument + Bar objects
- historical lot size is captured from NewBrdLotQty where present

## Next

- instrument master with valid_from / valid_to
- ZIP/raw archive ingestion
- index + India VIX adapters
- persistent Parquet writer
- option-chain snapshot schema

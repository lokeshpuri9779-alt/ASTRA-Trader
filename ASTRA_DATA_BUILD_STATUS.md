# ASTRA Data Build Status

Implemented:
- normalized Instrument / Bar / Quote schemas
- versioned historical instrument master
- OHLC/volume/OI validation
- quote crossed-market validation
- generic schema-driven CSV loader
- NSE UDiFF bhavcopy parser
- NSE index/India VIX style historical CSV loader
- normalized option-chain observation schema
- Parquet persistence adapter
- raw file SHA-256 ingestion manifests
- normalized bar -> replay Event adapter
- tests for validation, UDiFF ingestion, historical lot-size resolution and option spreads

Design principles:
- raw exchange files remain immutable
- historical instrument specifications are versioned
- exchange-specific formats map into stable ASTRA schemas
- option-chain snapshots are timestamped observations, not treated as historical truth unless actually archived at that time

Next:
1. raw ZIP/archive ingestion
2. persistent instrument master import/export
3. option-chain snapshot parser
4. India VIX and NIFTY source fixtures
5. replay fill/slippage engine

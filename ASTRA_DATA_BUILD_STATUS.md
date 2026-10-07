# ASTRA Data Build Status

Implemented:
- normalized Instrument / Bar / Quote schemas
- OHLC/volume/OI validation
- quote crossed-market validation
- schema-driven CSV loader
- normalized bar -> replay Event adapter
- tests for validation and event conversion

Design choice:
The loader is intentionally schema-driven rather than hardcoded to one NSE file layout. NSE publishes multiple report formats and can revise schemas. Source-specific parsers should map each official file into the stable ASTRA schema.

Next:
1. source-specific NSE UDiFF/bhavcopy parser
2. instrument-master versioning
3. raw-file hashing and ingestion manifests
4. India VIX/index history adapters
5. options/F&O contract normalization

# ASTRA Trader v1 Build Status

Implemented on the isolated `astra-v1-safety` branch:

## Core
- canonical event model
- explicit RESEARCH/PAPER/SHADOW/LIVE modes
- live execution disabled in application shell

## Trading safety
- deterministic risk engine
- score threshold
- daily loss limit
- loss-count limit
- open-risk cap
- spread/liquidity/volatility rejection
- kill switch
- paper broker

## Architecture
- market-data source interface
- strategy interface
- portfolio state
- order-intent/execution gateway abstraction
- health-state model

## Research infrastructure
- deterministic historical replay skeleton
- experiment manifest with SHA-256 identity
- append-only JSONL experiment ledger
- tests for replay and experiment recording

## Still intentionally missing
- real NSE historical ingestion
- realistic fill/slippage engine
- Indian fee engine
- options-chain normalizer
- walk-forward/CPCV runner
- strategy library
- INDmoney read-only adapter
- broker live execution

The next implementation milestone is the data ingestion + normalized market schema needed to feed the replay engine.

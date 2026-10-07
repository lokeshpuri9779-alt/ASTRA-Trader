# ASTRA Data Architecture

Status: research/design only. No live trading changes.

## Goals

ASTRA's data layer must support:
- reproducible research
- point-in-time backtesting
- event-driven replay
- Indian equities, indices, futures and options
- historical contract metadata
- auditability
- low risk of look-ahead contamination

## Canonical source hierarchy

### Tier 1 — Official exchange data
Prefer NSE-published files and reports for historical truth where available.

Use:
- F&O UDiFF common bhavcopy files
- contract-wise historical price/volume/open-interest data
- historical index data
- historical India VIX data
- daily/monthly market reports
- contract/master files and circulars for specification changes

Treat official exchange data as the canonical source for EOD and contract-history research.

### Tier 2 — Broker/authorized market data
Use broker or authorized feeds for:
- live/recent intraday candles
- quotes
- option-chain snapshots
- bid/ask
- streaming market data

Store raw payloads before normalization.

### Tier 3 — Derived data
ASTRA may calculate:
- returns
- realized volatility
- IV
- Greeks
- skew
- term structure
- futures basis
- OI changes
- PCR
- breadth
- regime labels
- technical features

Derived values must always retain lineage back to raw inputs and calculation version.

## Important distinction: option chain vs historical chain

The current NSE option-chain page is useful for live/current chain data but is not a complete historical point-in-time chain archive.

Do not reconstruct historical intraday option chains from today's page.

For historical options:
- use contract-level historical records for EOD studies,
- use officially licensed historical trades/order-book snapshots when intraday chain replay is required,
- or capture and persist our own live chain snapshots going forward.

## Point-in-time model

Every record should support two clocks where applicable:

- event_time: when the market event/observation occurred
- ingested_at: when ASTRA first received/stored it

Backtests query data by event_time but must enforce that ingested_at/data-version rules do not expose information that was unavailable then.

Also store:
- source
- source_file
- source_version/hash
- trading_date
- exchange timezone
- instrument identifier
- contract specification version

## Instrument master

Do not use symbol text alone as a permanent identifier.

Canonical instrument record should include:
- exchange
- segment
- instrument type
- underlying
- symbol
- expiry
- strike
- option type
- lot size
- tick size
- contract multiplier
- ISIN where relevant
- valid_from
- valid_to
- source/master-file version

Historical lot-size, expiry and contract-specification changes must be preserved instead of overwritten.

## Storage layout

Recommended local/research layout:

data/
  raw/
    nse/
      bhavcopy/
      indices/
      vix/
      masters/
      circulars/
      option_snapshots/
  normalized/
    instruments/
    equities/
    indices/
    futures/
    options/
  features/
  manifests/

Use Parquet for large immutable analytical datasets.

Use PostgreSQL (or another transactional DB) for:
- instrument master
- ingestion metadata
- strategy experiments
- orders/trades
- live state
- data manifests

Do not use a transactional DB as the only store for large historical tick datasets.

## Immutable raw zone

Never silently modify downloaded raw exchange files.

For each raw artifact record:
- URL/source
- retrieval timestamp
- SHA-256
- file size
- exchange date
- parser version

If NSE republishes/corrects a file, keep both versions and record which version a backtest used.

## Normalized schemas

### bars
- instrument_id
- timestamp
- interval
- open
- high
- low
- close
- volume
- open_interest
- source

### quotes
- instrument_id
- timestamp
- bid
- bid_qty
- ask
- ask_qty
- ltp
- volume
- open_interest

### option observations
- option_instrument_id
- underlying_instrument_id
- timestamp
- underlying_price
- expiry
- strike
- option_type
- bid
- ask
- ltp
- volume
- open_interest
- change_in_oi
- iv_source
- implied_volatility
- delta
- gamma
- theta
- vega

Greeks/IV calculated by ASTRA must be marked as derived and linked to pricing-model version/input assumptions.

## Backtest contamination controls

Reject datasets/backtests that violate any of these:

1. Current index membership used as if it existed historically.
2. Current lot size applied to old contracts.
3. Adjusted equity prices combined with unadjusted volume/events inconsistently.
4. Future corporate actions visible before announcement/effective time.
5. End-of-day OI used for an intraday decision before it was available.
6. Final daily high/low/close used inside the same day before close.
7. Today's option-chain values used to infer historical chain state.
8. Data corrections silently replacing the version used by prior experiments.
9. Random train/test splitting that leaks overlapping time-series labels.
10. Forward-filled prices through periods where the instrument was not actually tradable.

## Research data levels

### Level A — free/official EOD
Suitable for:
- equity momentum
- daily trend
- daily volatility
- futures/OI research
- coarse options research
- regime baselines

### Level B — broker intraday
Suitable for:
- intraday bars
- live paper trading
- spread/liquidity studies if quote data is available

### Level C — licensed historical tick/order-book data
Needed for credible research on:
- intraday options execution
- bid/ask microstructure
- partial fills
- expiry-day gamma strategies
- latency-sensitive setups

Do not claim microstructure alpha from EOD/candle data.

## India VIX

Use official NSE historical India VIX series as a regime/context input.

India VIX is based on NIFTY option order-book prices and represents expected near-term volatility; it should be treated as a market-volatility feature, not a directional signal.

## Ingestion pipeline

Source
-> raw immutable file/payload
-> hash/check
-> parser
-> schema validation
-> normalized tables/parquet
-> quality tests
-> feature pipeline
-> research manifest

A failed validation should quarantine the file rather than silently fill bad data.

## Data quality tests

At minimum:
- duplicate rows
- timestamp monotonicity
- impossible OHLC
- negative price/volume/OI
- missing contract master
- expiry mismatch
- strike/type mismatch
- quote crossed-market checks
- abnormal gap detection
- trading-calendar validation
- lot/tick-size consistency

## Experiment manifests

Every backtest must write a manifest containing:
- dataset hashes/versions
- date range
- universe definition
- instrument-master version
- feature-code version
- strategy commit SHA
- parameters
- fee/slippage model
- random seed
- result hash

A result without a manifest is not promotable.

## Initial ASTRA data plan

Phase 1:
- official NSE EOD indices
- official India VIX
- official F&O bhavcopy/UDiFF
- historical contract-wise F&O price/volume/OI
- instrument master/version history

Phase 2:
- broker/live quote and candle ingestion
- persistent option-chain snapshots
- paper-trading replay

Phase 3:
- licensed historical tick/order-book data only if a validated strategy needs it

This keeps initial research low-cost while preventing ASTRA from pretending candle/EOD data is sufficient for execution-sensitive options strategies.

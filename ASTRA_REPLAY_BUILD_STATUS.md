# ASTRA Replay Build Status

Implemented:
- deterministic market-event ordering
- replay strategy/risk evaluation
- bid/ask-aware market fill model
- volume participation cap and partial fills
- configurable basis-point slippage
- conservative bar stop gap-through handling
- versioned India cost-model hook
- STT rules effective from 1 April 2026 for option sales and futures sales
- tests for fills, partial fills, slippage, gap-through stops and STT

Still to implement:
- limit order fill logic
- order state machine integration
- margin/accounting ledger
- expiry settlement processor
- broker-style rejections
- latency scheduler
- portfolio P&L reconciliation

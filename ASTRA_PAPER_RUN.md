# Run ASTRA PAPER (no live trading)

This is a **single offline batch**, not a background daemon and not a live INDmoney feed. Use only authorized data and a time-stamped manifest from a separate collector.

Run:

```bash
python -m astra_trader.paper input.json journal.jsonl
python -m pytest -q test/test_astra_paper_session.py --noconftest
```

Minimal valid manifest (deliberately has no signal and produces no fills):

```json
{
  "observed_at": "2026-10-08T10:00:00+00:00",
  "risk_state": {"starting_capital": 100000, "current_equity": 100000},
  "signals": [],
  "quotes": {}
}
```

A strategy must separately produce genuine `TradeSignal` entries and a collector must supply quotes, each with a timezone-aware `timestamp` and `market` carrying bid, ask, last and volume. Quotes older than 120 seconds fail closed. A signal below score 78 is rejected. Partial simulated fills are possible. Every evaluated signal writes a journal entry.

Never confuse hypothetical fills with actual market executions. This runner has **no live broker API calls**, and **does not create fabricated trades** when signals or quote timestamps are absent.

Remaining for true unattended runs: authenticated external market-data collector with permitted runtime credentials, scheduled job/service, durable state and deployment, end-to-end integration testing.

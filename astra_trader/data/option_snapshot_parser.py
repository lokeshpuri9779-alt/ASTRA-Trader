from __future__ import annotations

from datetime import datetime

from .option_chain import OptionObservation

def parse_option_chain_snapshot(payload: dict, *, timestamp: datetime, underlying_id: str, source: str) -> list[OptionObservation]:
    records: list[OptionObservation] = []
    underlying_price = float(payload.get("underlyingValue") or payload.get("underlying_price") or 0)

    rows = payload.get("records") or payload.get("data") or []
    if isinstance(rows, dict):
        rows = rows.get("data", [])

    for row in rows:
        strike = float(row.get("strikePrice") or row.get("strike") or 0)
        expiry = str(row.get("expiryDate") or row.get("expiry") or "")
        for key, option_type in (("CE","CE"),("PE","PE")):
            leg = row.get(key)
            if not leg:
                continue
            bid = leg.get("bidprice") if "bidprice" in leg else leg.get("bidPrice")
            ask = leg.get("askPrice")
            obs = OptionObservation(
                option_instrument_id=str(leg.get("identifier") or f"{underlying_id}:{expiry}:{strike}:{option_type}"),
                underlying_instrument_id=underlying_id,
                timestamp=timestamp,
                underlying_price=float(leg.get("underlyingValue") or underlying_price),
                expiry=expiry,
                strike=strike,
                option_type=option_type,
                bid=float(bid) if bid not in (None,"") else None,
                bid_qty=float(leg.get("bidQty")) if leg.get("bidQty") not in (None,"") else None,
                ask=float(ask) if ask not in (None,"") else None,
                ask_qty=float(leg.get("askQty")) if leg.get("askQty") not in (None,"") else None,
                ltp=float(leg.get("lastPrice")) if leg.get("lastPrice") not in (None,"") else None,
                volume=float(leg.get("totalTradedVolume")) if leg.get("totalTradedVolume") not in (None,"") else None,
                open_interest=float(leg.get("openInterest")) if leg.get("openInterest") not in (None,"") else None,
                change_in_open_interest=float(leg.get("changeinOpenInterest")) if leg.get("changeinOpenInterest") not in (None,"") else None,
                implied_volatility=float(leg.get("impliedVolatility")) if leg.get("impliedVolatility") not in (None,"") else None,
                source=source,
            )
            records.append(obs)
    return records

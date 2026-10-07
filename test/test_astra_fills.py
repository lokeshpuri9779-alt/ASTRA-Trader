from astra_trader.replay.fills import FillModel, MarketSnapshot, Side
from astra_trader.replay.stops import stop_market_fill

def test_buy_crosses_ask_and_respects_volume_cap():
    model = FillModel(max_volume_participation=0.10, slippage_bps=10)
    fill = model.market_fill(
        side=Side.BUY,
        quantity=100,
        snapshot=MarketSnapshot(bid=99, ask=100, last=99.5, volume=500),
    )
    assert fill is not None
    assert fill.quantity == 50
    assert fill.partial
    assert round(fill.price, 4) == 100.1

def test_sell_crosses_bid():
    model = FillModel()
    fill = model.market_fill(
        side=Side.SELL,
        quantity=10,
        snapshot=MarketSnapshot(bid=99, ask=100, last=99.5, volume=1000),
    )
    assert fill is not None
    assert fill.price == 99

def test_stop_gap_through_uses_next_open():
    result = stop_market_fill(side="SELL", stop_price=100, next_open=95, next_low=94, next_high=101)
    assert result.triggered
    assert result.fill_price == 95

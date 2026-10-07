from pathlib import Path

from astra_trader.paper.divergence import compare_execution
from astra_trader.paper.order_book import SimulatedOrderBook
from astra_trader.paper.portfolio_store import load_paper_portfolio, save_paper_portfolio
from astra_trader.paper.shadow import ShadowGateway, ShadowIntent
from astra_trader.replay.accounting import AccountLedger
from astra_trader.replay.order_state import SimulatedOrder

def test_order_book_and_shadow():
    b=SimulatedOrderBook()
    b.add(SimulatedOrder("1","X","BUY",10))
    assert len(b.open_orders())==1
    s=ShadowGateway()
    s.submit(ShadowIntent("X","BUY",10,100))
    assert len(s.intents)==1

def test_paper_portfolio_roundtrip(tmp_path: Path):
    l=AccountLedger(cash=10000)
    l.apply_fill(symbol="X",side="BUY",quantity=5,price=100)
    p=save_paper_portfolio(l,tmp_path/"portfolio.json")
    r=load_paper_portfolio(p)
    assert r.positions["X"]==5

def test_divergence():
    d=compare_execution(
        replay_price=100,observed_shadow_price=101,
        replay_qty=10,shadow_qty=9,replay_pnl=100,shadow_pnl=80,
    )
    assert d.fill_price_bps>0 and d.quantity_difference==-1 and d.pnl_difference==-20

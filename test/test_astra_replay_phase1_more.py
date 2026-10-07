from astra_trader.replay.accounting import SimulationLedger
from astra_trader.replay.order_state import OrderState, SimulatedOrder
from astra_trader.replay.reconcile import reconcile_ledger
from astra_trader.replay.rejections import RejectionPolicy

def test_order_state_machine():
    o=SimulatedOrder("id","NIFTY","BUY",10)
    o.transition(OrderState.ACKNOWLEDGED)
    o.apply_fill(4,100)
    assert o.state is OrderState.PARTIALLY_FILLED
    o.apply_fill(6,101)
    assert o.state is OrderState.FILLED

def test_rejections():
    p=RejectionPolicy(max_order_quantity=100)
    assert p.evaluate(quantity=25,lot_size=50,has_market_data=True)=="INVALID_LOT_SIZE"
    assert p.evaluate(quantity=50,lot_size=50,has_market_data=False)=="MISSING_MARKET_DATA"
    assert p.evaluate(quantity=50,lot_size=50,has_market_data=True,available_cash=100,required_cash=200)=="INSUFFICIENT_CASH"

def test_accounting_and_reconciliation():
    l=SimulationLedger(10000)
    l.apply_fill(symbol="X",side="BUY",quantity=10,price=100,fee=5)
    l.apply_fill(symbol="X",side="SELL",quantity=4,price=110,fee=5)
    r=reconcile_ledger(l,{"X":105})
    assert round(r.realized_pnl,6)==40
    assert round(r.unrealized_pnl,6)==30
    assert r.fees==10

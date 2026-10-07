from astra_trader.integrations.indmoney import IndMoneyPosition
from astra_trader.integrations.indmoney_capabilities import OFFICIAL_INDMONEY_CAPABILITIES
from astra_trader.integrations.indmoney_guard import assert_indmoney_read_only, assert_no_indmoney_execution
from astra_trader.integrations.indmoney_normalize import normalize_positions
from astra_trader.integrations.indmoney_reconcile import reconcile_indmoney_positions

def test_indmoney_is_strictly_read_only():
    assert OFFICIAL_INDMONEY_CAPABILITIES.read_only
    assert not OFFICIAL_INDMONEY_CAPABILITIES.order_write
    assert_indmoney_read_only()
    assert_no_indmoney_execution()

def test_indmoney_position_reconciliation():
    rows=[IndMoneyPosition("ABC",10,average_price=100,current_price=105)]
    p=normalize_positions(rows,cash=1000)
    r=reconcile_indmoney_positions(p,rows)
    assert r.ok
    r2=reconcile_indmoney_positions(p,[IndMoneyPosition("ABC",9)])
    assert not r2.ok and r2.mismatches==("ABC",)

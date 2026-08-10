from datetime import datetime

import pytest

from execution.order_poller import OrderPoller
from portfolio.trade_ledger import TradeEvent, TradeLedger


@pytest.fixture
def ledger():
    return TradeLedger()


def make_trade(symbol="NIFTY", side="BUY", qty=1, price=100):
    return TradeEvent(
        symbol=symbol,
        side=side,
        qty=qty,
        price=price,
        timestamp=datetime.now(),
        order_id="test-order",
    )


def test_single_buy_no_pnl(ledger):
    ledger.record_trade(make_trade(side="BUY", qty=10, price=100))

    assert ledger.realized_pnl == 0
    assert len(ledger.open_positions) == 1


def test_simple_pnl(ledger):
    ledger.record_trade(make_trade("NIFTY", "BUY", 10, 100))
    ledger.record_trade(make_trade("NIFTY", "SELL", 10, 120))

    assert round(ledger.realized_pnl, 2) == 200
    assert len(ledger.open_positions) == 0


def test_fifo_matching(ledger):
    ledger.record_trade(make_trade(price=100, qty=10))
    ledger.record_trade(make_trade(price=110, qty=10))

    ledger.record_trade(make_trade(side="SELL", price=120, qty=15))

    assert round(ledger.realized_pnl, 2) == 250


def test_partial_fills(ledger):
    ledger.record_trade(make_trade(qty=3, price=100))
    ledger.record_trade(make_trade(qty=4, price=100))
    ledger.record_trade(make_trade(qty=3, price=100))

    ledger.record_trade(make_trade(side="SELL", qty=10, price=110))

    assert round(ledger.realized_pnl, 2) == 100


def test_partial_sell_across_buys(ledger):
    ledger.record_trade(make_trade(qty=5, price=100))
    ledger.record_trade(make_trade(qty=5, price=110))

    ledger.record_trade(make_trade(side="SELL", qty=7, price=120))

    # (5 * 20) + (2 * 10) = 100 + 20 = 120
    assert round(ledger.realized_pnl, 2) == 120


def test_unrealized_pnl(ledger):
    ledger.record_trade(make_trade(qty=10, price=100))

    pnl = ledger.get_unrealized_pnl(current_price=110)

    assert pnl == 100


def test_sell_without_position(ledger):
    with pytest.raises(ValueError):
        ledger.record_trade(make_trade(side="SELL", qty=5, price=100))


def test_order_poller_updates_ledger(mocker, ledger):
    mock_order_service = mocker.Mock()
    mock_position_manager = mocker.Mock()

    poller = OrderPoller(order_service=mock_order_service, position_manager=mock_position_manager)

    poller.trade_ledger = ledger

    mock_fill = mocker.Mock(
        side="BUY",
        qty=5,
        price=100,
        timestamp=datetime.now(),
        symbol="NIFTY",
        order_id="test-order",
    )

    poller._handle_fill(mock_fill)

    assert len(ledger.trades) == 1


def test_sell_more_than_available_should_fail(ledger):
    ledger.record_trade(make_trade(qty=5, price=100))

    with pytest.raises(ValueError):
        ledger.record_trade(make_trade(side="SELL", qty=10, price=120))

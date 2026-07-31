from backtesting.commission import Commission


def test_commission_reduces_pnl():
    trade = {
        "pnl": 100,
    }

    commission = Commission(amount=20)

    result = commission.apply(trade)

    assert result["pnl"] == 80


def test_original_trade_is_not_modified():
    trade = {
        "pnl": 100,
    }

    commission = Commission(amount=20)

    commission.apply(trade)

    assert trade["pnl"] == 100

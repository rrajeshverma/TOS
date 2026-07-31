import pytest

from paper.paper_portfolio import PaperPortfolio


def test_can_create_portfolio():
    assert PaperPortfolio() is not None


def test_initial_cash():
    portfolio = PaperPortfolio()

    assert portfolio.cash == 1_000_000


def test_buy_reduces_cash():
    portfolio = PaperPortfolio()

    portfolio.buy("NIFTY", 10, 25000)

    assert portfolio.cash == 750000


def test_sell_increases_cash():
    portfolio = PaperPortfolio()

    portfolio.sell("NIFTY", 10, 25000)

    assert portfolio.cash == 1250000


def test_records_position():
    portfolio = PaperPortfolio()

    portfolio.buy("NIFTY", 5, 25000)

    assert portfolio.position("NIFTY") == 5


def test_multiple_positions():
    portfolio = PaperPortfolio()

    portfolio.buy("NIFTY", 5, 25000)
    portfolio.buy("BANKNIFTY", 2, 55000)

    assert len(portfolio.positions()) == 2


def test_unknown_position():
    portfolio = PaperPortfolio()

    assert portfolio.position("ABC") == 0


def test_equity_initial():
    portfolio = PaperPortfolio()

    assert portfolio.equity() == 1_000_000


def test_buy_then_sell():
    portfolio = PaperPortfolio()

    portfolio.buy("NIFTY", 5, 25000)
    portfolio.sell("NIFTY", 5, 25000)

    assert portfolio.position("NIFTY") == 0


def test_reject_negative_quantity():
    portfolio = PaperPortfolio()

    with pytest.raises(ValueError):
        portfolio.buy("NIFTY", -1, 25000)


def test_reject_zero_price():
    portfolio = PaperPortfolio()

    with pytest.raises(ValueError):
        portfolio.buy("NIFTY", 1, 0)


def test_repeatable():
    portfolio = PaperPortfolio()

    assert portfolio.equity() == portfolio.equity()


def test_stateless_query():
    portfolio = PaperPortfolio()

    portfolio.positions()

    assert portfolio.equity() == 1_000_000


def test_cash_after_multiple_trades():
    portfolio = PaperPortfolio()

    portfolio.buy("NIFTY", 2, 100)
    portfolio.buy("BANKNIFTY", 3, 200)

    assert portfolio.cash == 999200


def test_position_count():
    portfolio = PaperPortfolio()

    portfolio.buy("NIFTY", 1, 100)

    assert len(portfolio.positions()) == 1

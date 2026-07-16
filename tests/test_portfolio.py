import pytest

from domain.portfolio import Portfolio


def test_portfolio_creation():
    portfolio = Portfolio(
        account_id="ACC123",
        cash=100000.0,
        available_margin=80000.0,
        used_margin=20000.0,
        equity=100000.0,
        realized_pnl=500.0,
        unrealized_pnl=250.0,
        positions=2,
        holdings=1,
    )

    assert portfolio.account_id == "ACC123"
    assert portfolio.cash == 100000.0


def test_total_funds():
    portfolio = Portfolio(
        account_id="ACC123",
        cash=100000.0,
        available_margin=80000.0,
        used_margin=20000.0,
        equity=100000.0,
        realized_pnl=500.0,
        unrealized_pnl=250.0,
        positions=2,
        holdings=1,
    )

    assert portfolio.total_funds() == 100000.0


def test_free_margin():
    portfolio = Portfolio(
        account_id="ACC123",
        cash=100000.0,
        available_margin=80000.0,
        used_margin=20000.0,
        equity=100000.0,
        realized_pnl=500.0,
        unrealized_pnl=250.0,
        positions=2,
        holdings=1,
    )

    assert portfolio.free_margin() == 80000.0


def test_to_dict():
    portfolio = Portfolio(
        account_id="ACC123",
        cash=100000.0,
        available_margin=80000.0,
        used_margin=20000.0,
        equity=100000.0,
        realized_pnl=500.0,
        unrealized_pnl=250.0,
        positions=2,
        holdings=1,
    )

    data = portfolio.to_dict()

    assert data["account_id"] == "ACC123"
    assert data["cash"] == 100000.0


def test_from_dict():
    data = {
        "account_id": "ACC123",
        "cash": 100000.0,
        "available_margin": 80000.0,
        "used_margin": 20000.0,
        "equity": 100000.0,
        "realized_pnl": 500.0,
        "unrealized_pnl": 250.0,
        "positions": 2,
        "holdings": 1,
    }

    portfolio = Portfolio.from_dict(data)

    assert portfolio.account_id == "ACC123"
    assert portfolio.cash == 100000.0
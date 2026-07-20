from tests.helpers.domain_factory import (
    make_trade,
    make_portfolio,
)


def test_make_trade():

    trade = make_trade()

    assert trade is not None


def test_make_portfolio():

    portfolio = make_portfolio()

    assert portfolio.account_id == "ACC001"
from portfolio.portfolio_engine import PortfolioEngine


def test_portfolio_engine_can_be_created():

    engine = PortfolioEngine()

    assert engine is not None


def test_engine_requires_portfolio_context():

    engine = PortfolioEngine()

    result = engine.evaluate(
        None
    )

    assert result is None


def test_engine_calculates_exposure():

    engine = PortfolioEngine()

    context = {
        "positions": [
            {
                "symbol": "NIFTY",
                "quantity": 10,
                "price": 20000,
            }
        ],
        "capital": 100000,
    }

    result = engine.evaluate(
        context
    )

    assert (
        result["exposure"]
        == 200000
    )


def test_engine_returns_allocation():

    engine = PortfolioEngine()

    context = {
        "positions": [],
        "capital": 100000,
        "allocation": {
            "NIFTY": 50,
        },
    }

    result = engine.evaluate(
        context
    )

    assert (
        result["allocation"]["NIFTY"]
        == 50000
    )


def test_engine_contains_portfolio_status():

    engine = PortfolioEngine()

    context = {
        "positions": [],
        "capital": 100000,
    }

    result = engine.evaluate(
        context
    )

    assert (
        "status"
        in result
    )


def test_engine_marks_ready_portfolio():

    engine = PortfolioEngine()

    context = {
        "positions": [],
        "capital": 100000,
    }

    result = engine.evaluate(
        context
    )

    assert (
        result["status"]
        == "READY"
    )

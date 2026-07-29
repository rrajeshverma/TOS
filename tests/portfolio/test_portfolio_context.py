from portfolio.portfolio_context import PortfolioContext


def test_portfolio_context_can_be_created():
    context = PortfolioContext(
        cash=100000,
        positions=[],
        exposure=0,
        available_margin=100000,
        pnl=0,
    )

    assert context.cash == 100000
    assert context.positions == []
    assert context.exposure == 0
    assert context.available_margin == 100000
    assert context.pnl == 0


def test_portfolio_context_is_immutable():
    context = PortfolioContext(
        cash=100000,
        positions=[],
        exposure=0,
        available_margin=100000,
        pnl=0,
    )

    try:
        context.cash = 50000
        assert False

    except Exception:
        assert True


def test_portfolio_context_requires_cash():
    try:
        PortfolioContext(
            cash=None,
            positions=[],
            exposure=0,
            available_margin=100000,
            pnl=0,
        )

        assert False

    except ValueError:
        assert True


def test_portfolio_context_requires_positions():
    try:
        PortfolioContext(
            cash=100000,
            positions=None,
            exposure=0,
            available_margin=100000,
            pnl=0,
        )

        assert False

    except ValueError:
        assert True


def test_portfolio_context_rejects_negative_margin():
    try:
        PortfolioContext(
            cash=100000,
            positions=[],
            exposure=0,
            available_margin=-1,
            pnl=0,
        )

        assert False

    except ValueError:
        assert True


def test_portfolio_context_stores_profit_loss():
    context = PortfolioContext(
        cash=100000,
        positions=[],
        exposure=10000,
        available_margin=90000,
        pnl=2500,
    )

    assert context.pnl == 2500

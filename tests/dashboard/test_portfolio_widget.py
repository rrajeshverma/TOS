from dashboard.widgets.portfolio_widget import PortfolioWidget


def test_portfolio_widget_defaults():
    widget = PortfolioWidget()

    assert widget.cash == 0.0
    assert widget.exposure == 0.0
    assert widget.pnl == 0.0
    assert widget.positions == 0


def test_portfolio_widget_custom_values():
    widget = PortfolioWidget(
        cash=850000,
        exposure=125000,
        pnl=8420,
        positions=3,
    )

    assert widget.cash == 850000
    assert widget.exposure == 125000
    assert widget.pnl == 8420
    assert widget.positions == 3


def test_portfolio_widget_render():
    widget = PortfolioWidget(
        cash=875000,
        exposure=124000,
        pnl=8420,
        positions=3,
    )

    output = widget.render()

    assert "Portfolio" in output
    assert "875,000.00" in output
    assert "124,000.00" in output
    assert "8,420.00" in output
    assert "3" in output

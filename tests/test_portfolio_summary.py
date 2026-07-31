from dashboard.widgets.portfolio_summary import PortfolioSummary


def test_portfolio_summary_defaults():
    summary = PortfolioSummary()

    assert summary.total_value == 0.0
    assert summary.cash == 0.0
    assert summary.invested == 0.0
    assert summary.pnl == 0.0

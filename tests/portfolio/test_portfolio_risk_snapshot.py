from portfolio.portfolio_risk import PortfolioRisk
from portfolio.portfolio_snapshot import PortfolioSnapshot


def test_update_risk_from_snapshot():
    risk = PortfolioRisk(
        100000,
        2,
    )

    snapshot = PortfolioSnapshot(
        cash=100000,
        equity=98500,
        realized_pnl=-500,
        unrealized_pnl=-1000,
        open_positions=1,
    )

    risk.update_from_snapshot(snapshot)

    assert risk.current_risk == 1500


def test_positive_profit_does_not_create_risk():
    risk = PortfolioRisk(
        100000,
        2,
    )

    snapshot = PortfolioSnapshot(
        cash=100000,
        equity=101500,
        realized_pnl=1000,
        unrealized_pnl=500,
        open_positions=1,
    )

    risk.update_from_snapshot(snapshot)

    assert risk.current_risk == 0

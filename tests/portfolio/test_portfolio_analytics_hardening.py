from portfolio.portfolio_snapshot import PortfolioSnapshot
from portfolio.portfolio_metrics import PortfolioMetrics
from portfolio.portfolio_risk import PortfolioRisk


def create_snapshot():
    return PortfolioSnapshot(
        cash=100000,
        equity=110000,
        realized_pnl=5000,
        unrealized_pnl=5000,
        open_positions=2,
    )


# -------------------------
# Snapshot Tests
# -------------------------


def test_snapshot_to_dict():
    snapshot = create_snapshot()

    result = snapshot.to_dict()

    assert result["cash"] == 100000


def test_snapshot_total_pnl():
    snapshot = create_snapshot()

    assert snapshot.total_pnl() == 10000


def test_snapshot_profitable():
    snapshot = create_snapshot()

    assert snapshot.is_profitable()


def test_snapshot_has_positions():
    snapshot = create_snapshot()

    assert snapshot.has_open_positions()


def test_snapshot_flat():
    snapshot = PortfolioSnapshot(
        100,
        100,
        0,
        0,
        0,
    )

    assert snapshot.is_flat()


def test_increment_positions():
    snapshot = create_snapshot()

    snapshot.increment_positions()

    assert snapshot.open_positions == 3


def test_decrement_positions():
    snapshot = create_snapshot()

    snapshot.decrement_positions()

    assert snapshot.open_positions == 1


def test_deposit():
    snapshot = create_snapshot()

    snapshot.deposit(1000)

    assert snapshot.cash == 101000


def test_withdraw():
    snapshot = create_snapshot()

    snapshot.withdraw(5000)

    assert snapshot.cash == 95000


def test_snapshot_copy():
    snapshot = create_snapshot()

    copy = snapshot.copy()

    assert copy.to_dict() == snapshot.to_dict()


# -------------------------
# Metrics Tests
# -------------------------


def test_metrics_total_pnl():
    metrics = PortfolioMetrics()

    assert metrics.total_pnl(create_snapshot()) == 10000


def test_return_percent():
    metrics = PortfolioMetrics()

    assert metrics.return_percent(create_snapshot()) == 10


def test_cash_ratio():
    metrics = PortfolioMetrics()

    assert round(metrics.cash_ratio(create_snapshot()), 2) == 90.91


def test_equity_change():
    metrics = PortfolioMetrics()

    assert metrics.equity_change(create_snapshot()) == 10000


def test_portfolio_is_growing():
    metrics = PortfolioMetrics()

    assert metrics.is_growing(create_snapshot())


# -------------------------
# Risk Tests
# -------------------------


def test_maximum_risk():
    risk = PortfolioRisk(
        100000,
        2,
    )

    assert risk.maximum_risk() == 2000


def test_remaining_risk():
    risk = PortfolioRisk(
        100000,
        2,
    )

    risk.current_risk = 500

    assert risk.remaining_risk() == 1500


def test_exposure_percent():
    risk = PortfolioRisk(
        100000,
        2,
    )

    risk.current_risk = 1000

    assert risk.exposure_percent() == 50


def test_can_open_position():
    risk = PortfolioRisk(
        100000,
        2,
    )

    assert risk.can_open_position()


def test_risk_summary():
    risk = PortfolioRisk(
        100000,
        2,
    )

    summary = risk.summary()

    assert "maximum_risk" in summary

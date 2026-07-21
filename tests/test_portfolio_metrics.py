from portfolio.portfolio_metrics import PortfolioMetrics
from portfolio.portfolio_snapshot import PortfolioSnapshot


def test_total_pnl():
    snapshot = PortfolioSnapshot(
        cash=100000,
        equity=101500,
        realized_pnl=1000,
        unrealized_pnl=500,
        open_positions=2,
    )

    metrics = PortfolioMetrics()

    assert metrics.total_pnl(snapshot) == 1500


def test_return_percent():
    snapshot = PortfolioSnapshot(
        cash=100000,
        equity=101500,
        realized_pnl=1000,
        unrealized_pnl=500,
        open_positions=2,
    )

    metrics = PortfolioMetrics()

    assert metrics.return_percent(snapshot) == 1.5


def test_cash_ratio():
    snapshot = PortfolioSnapshot(
        cash=80000,
        equity=100000,
        realized_pnl=0,
        unrealized_pnl=0,
        open_positions=2,
    )

    metrics = PortfolioMetrics()

    assert metrics.cash_ratio(snapshot) == 80.0


def test_summary():
    snapshot = PortfolioSnapshot(
        cash=80000,
        equity=100000,
        realized_pnl=1000,
        unrealized_pnl=500,
        open_positions=2,
    )

    metrics = PortfolioMetrics()

    summary = metrics.summary(snapshot)

    assert summary["total_pnl"] == 1500
    assert summary["return_percent"] == 1.875
    assert summary["cash_ratio"] == 80.0


# ============================================================
# Equity Metrics
# ============================================================


def test_equity_change_positive():
    snapshot = PortfolioSnapshot(100000, 101500, 1000, 500, 2)

    metrics = PortfolioMetrics()

    assert metrics.equity_change(snapshot) == 1500


def test_equity_change_negative():
    snapshot = PortfolioSnapshot(100000, 98500, -1000, -500, 1)

    metrics = PortfolioMetrics()

    assert metrics.equity_change(snapshot) == -1500


def test_equity_gain():
    snapshot = PortfolioSnapshot(100000, 103000, 2000, 1000, 2)

    metrics = PortfolioMetrics()

    assert metrics.equity_gain(snapshot) == 3000


def test_equity_change_zero():
    snapshot = PortfolioSnapshot(100000, 100000, 0, 0, 0)

    metrics = PortfolioMetrics()

    assert metrics.equity_change(snapshot) == 0


# ============================================================
# Portfolio Health
# ============================================================


def test_is_growing():
    snapshot = PortfolioSnapshot(100000, 101000, 1000, 0, 1)

    metrics = PortfolioMetrics()

    assert metrics.is_growing(snapshot) is True


def test_is_not_growing():
    snapshot = PortfolioSnapshot(100000, 99000, -1000, 0, 1)

    metrics = PortfolioMetrics()

    assert metrics.is_growing(snapshot) is False


def test_is_in_drawdown():
    snapshot = PortfolioSnapshot(100000, 98000, -1500, -500, 1)

    metrics = PortfolioMetrics()

    assert metrics.is_in_drawdown(snapshot) is True


def test_not_in_drawdown():
    snapshot = PortfolioSnapshot(100000, 101000, 1000, 0, 1)

    metrics = PortfolioMetrics()

    assert metrics.is_in_drawdown(snapshot) is False


# ============================================================
# Exposure
# ============================================================


def test_position_exposure_zero():
    snapshot = PortfolioSnapshot(100000, 100000, 0, 0, 0)

    metrics = PortfolioMetrics()

    assert metrics.position_exposure(snapshot) == 0


def test_position_exposure_single():
    snapshot = PortfolioSnapshot(100000, 100000, 0, 0, 1)

    metrics = PortfolioMetrics()

    assert metrics.position_exposure(snapshot) == 1


def test_position_exposure_multiple():
    snapshot = PortfolioSnapshot(100000, 100000, 0, 0, 5)

    metrics = PortfolioMetrics()

    assert metrics.position_exposure(snapshot) == 5


def test_cash_utilization():
    snapshot = PortfolioSnapshot(80000, 100000, 0, 0, 2)

    metrics = PortfolioMetrics()

    assert metrics.cash_utilization(snapshot) == 20.0


# ============================================================
# Summary
# ============================================================


def test_summary_contains_total_pnl():
    snapshot = PortfolioSnapshot(100000, 101500, 1000, 500, 2)

    summary = PortfolioMetrics().summary(snapshot)

    assert summary["total_pnl"] == 1500


def test_summary_contains_equity_change():
    snapshot = PortfolioSnapshot(100000, 101500, 1000, 500, 2)

    summary = PortfolioMetrics().summary(snapshot)

    assert summary["equity_change"] == 1500


def test_summary_contains_return_percent():
    snapshot = PortfolioSnapshot(100000, 101500, 1000, 500, 2)

    summary = PortfolioMetrics().summary(snapshot)

    assert summary["return_percent"] == 1.5


def test_summary_contains_cash_ratio():
    snapshot = PortfolioSnapshot(80000, 100000, 1000, 500, 2)

    summary = PortfolioMetrics().summary(snapshot)

    assert summary["cash_ratio"] == 80.0


def test_summary_contains_profit_flag():
    snapshot = PortfolioSnapshot(100000, 101500, 1000, 500, 2)

    summary = PortfolioMetrics().summary(snapshot)

    assert summary["is_profitable"] is True


def test_summary_contains_position_flag():
    snapshot = PortfolioSnapshot(100000, 101500, 1000, 500, 2)

    summary = PortfolioMetrics().summary(snapshot)

    assert summary["has_open_positions"] is True


def test_summary_contains_position_count():
    snapshot = PortfolioSnapshot(100000, 101500, 1000, 500, 3)

    summary = PortfolioMetrics().summary(snapshot)

    assert summary["position_count"] == 3


def test_summary_contains_cash():
    snapshot = PortfolioSnapshot(75000, 76000, 500, 500, 1)

    summary = PortfolioMetrics().summary(snapshot)

    assert summary["cash"] == 75000

def test_return_percent_zero_cash():
    snapshot = PortfolioSnapshot(
        cash=0,
        equity=100000,
        realized_pnl=1000,
        unrealized_pnl=500,
        open_positions=1,
    )

    metrics = PortfolioMetrics()

    assert metrics.return_percent(snapshot) == 0.0


def test_cash_ratio_zero_equity():
    snapshot = PortfolioSnapshot(
        cash=100000,
        equity=0,
        realized_pnl=0,
        unrealized_pnl=0,
        open_positions=0,
    )

    metrics = PortfolioMetrics()

    assert metrics.cash_ratio(snapshot) == 0.0


def test_cash_utilization_zero_equity():
    snapshot = PortfolioSnapshot(
        cash=100000,
        equity=0,
        realized_pnl=0,
        unrealized_pnl=0,
        open_positions=0,
    )

    metrics = PortfolioMetrics()

    assert metrics.cash_utilization(snapshot) == 0.0
import pytest

from reporting.models.performance_model import PerformanceModel
from reporting.services.performance_service import PerformanceService


class DummyTrade:
    def __init__(self, pnl=0.0):
        self.pnl = pnl


def test_calculate_empty_performance():
    service = PerformanceService()

    model = service.calculate([])

    assert isinstance(model, PerformanceModel)
    assert model.total_trades == 0
    assert model.winning_trades == 0
    assert model.losing_trades == 0
    assert model.net_profit == 0.0


def test_calculate_total_trades():
    service = PerformanceService()

    trades = [
        DummyTrade(),
        DummyTrade(),
        DummyTrade(),
    ]

    model = service.calculate(trades)

    assert model.total_trades == 3


def test_calculate_winning_and_losing_trades():
    service = PerformanceService()

    trades = [
        DummyTrade(100.0),
        DummyTrade(-50.0),
        DummyTrade(75.0),
        DummyTrade(-25.0),
    ]

    model = service.calculate(trades)

    assert model.total_trades == 4
    assert model.winning_trades == 2
    assert model.losing_trades == 2


def test_calculate_net_profit():
    service = PerformanceService()

    trades = [
        DummyTrade(100.0),
        DummyTrade(-40.0),
        DummyTrade(60.0),
        DummyTrade(-20.0),
    ]

    model = service.calculate(trades)

    assert model.net_profit == 100.0


def test_calculate_gross_profit():
    service = PerformanceService()

    trades = [
        DummyTrade(100.0),
        DummyTrade(-40.0),
        DummyTrade(60.0),
        DummyTrade(-20.0),
    ]

    model = service.calculate(trades)

    assert model.gross_profit == 160.0


def test_calculate_gross_loss():
    service = PerformanceService()

    trades = [
        DummyTrade(100.0),
        DummyTrade(-40.0),
        DummyTrade(60.0),
        DummyTrade(-20.0),
    ]

    model = service.calculate(trades)

    assert model.gross_loss == 60.0


def test_calculate_win_rate():
    service = PerformanceService()

    trades = [
        DummyTrade(100.0),
        DummyTrade(-40.0),
        DummyTrade(60.0),
        DummyTrade(-20.0),
    ]

    model = service.calculate(trades)

    assert model.win_rate == 50.0


def test_calculate_profit_factor():
    service = PerformanceService()

    trades = [
        DummyTrade(100.0),
        DummyTrade(-40.0),
        DummyTrade(60.0),
        DummyTrade(-20.0),
    ]

    model = service.calculate(trades)

    assert model.profit_factor == pytest.approx(160.0 / 60.0)


def test_calculate_average_win_and_loss():
    service = PerformanceService()

    trades = [
        DummyTrade(100.0),
        DummyTrade(60.0),
        DummyTrade(-40.0),
        DummyTrade(-20.0),
    ]

    model = service.calculate(trades)

    assert model.average_win == 80.0
    assert model.average_loss == 30.0


def test_calculate_largest_win_and_loss():
    service = PerformanceService()

    trades = [
        DummyTrade(100.0),
        DummyTrade(60.0),
        DummyTrade(-40.0),
        DummyTrade(-20.0),
    ]

    model = service.calculate(trades)

    assert model.largest_win == 100.0
    assert model.largest_loss == 40.0


def test_calculate_expectancy():
    service = PerformanceService()

    trades = [
        DummyTrade(100.0),
        DummyTrade(60.0),
        DummyTrade(-40.0),
        DummyTrade(-20.0),
    ]

    model = service.calculate(trades)

    assert model.expectancy == pytest.approx(25.0)


def test_calculate_equity_curve():
    service = PerformanceService()

    trades = [
        DummyTrade(100.0),
        DummyTrade(-40.0),
        DummyTrade(60.0),
    ]

    model = service.calculate(trades)

    assert model.equity_curve == [100.0, 60.0, 120.0]


def test_calculate_max_drawdown():
    service = PerformanceService()

    trades = [
        DummyTrade(100.0),
        DummyTrade(50.0),
        DummyTrade(-30.0),
        DummyTrade(60.0),
        DummyTrade(-70.0),
    ]

    model = service.calculate(trades)

    assert model.equity_curve == [100.0, 150.0, 120.0, 180.0, 110.0]
    assert model.max_drawdown == 70.0


def test_calculate_max_drawdown_percent():
    service = PerformanceService()

    trades = [
        DummyTrade(100.0),
        DummyTrade(50.0),
        DummyTrade(-30.0),
        DummyTrade(60.0),
        DummyTrade(-70.0),
    ]

    model = service.calculate(trades)

    assert model.max_drawdown == 70.0
    assert model.max_drawdown_percent == pytest.approx((70.0 / 180.0) * 100)


def test_calculate_peak_equity():
    service = PerformanceService()

    trades = [
        DummyTrade(100.0),
        DummyTrade(50.0),
        DummyTrade(-30.0),
        DummyTrade(60.0),
        DummyTrade(-70.0),
    ]

    model = service.calculate(trades)

    assert model.peak_equity == 180.0


def test_calculate_recovery_factor():
    service = PerformanceService()

    trades = [
        DummyTrade(100.0),
        DummyTrade(50.0),
        DummyTrade(-30.0),
        DummyTrade(60.0),
        DummyTrade(-70.0),
    ]

    model = service.calculate(trades)

    assert model.recovery_factor == pytest.approx(110.0 / 70.0)


def test_calculate_max_consecutive_wins():
    service = PerformanceService()

    trades = [
        DummyTrade(100.0),  # W
        DummyTrade(50.0),  # W
        DummyTrade(-20.0),  # L
        DummyTrade(80.0),  # W
        DummyTrade(40.0),  # W
        DummyTrade(60.0),  # W
        DummyTrade(-10.0),  # L
    ]

    model = service.calculate(trades)

    assert model.max_consecutive_wins == 3


def test_calculate_max_consecutive_losses():
    service = PerformanceService()

    trades = [
        DummyTrade(-20.0),  # L
        DummyTrade(-10.0),  # L
        DummyTrade(50.0),  # W
        DummyTrade(-30.0),  # L
        DummyTrade(-40.0),  # L
        DummyTrade(-15.0),  # L
        DummyTrade(60.0),  # W
    ]

    model = service.calculate(trades)

    assert model.max_consecutive_losses == 3

def test_calculate_trade_counts_helper():
    service = PerformanceService()
    model = PerformanceModel()

    trades = [
        DummyTrade(100.0),
        DummyTrade(-50.0),
        DummyTrade(75.0),
        DummyTrade(0.0),
    ]

    service._calculate_trade_counts(
        model,
        trades,
    )

    assert model.total_trades == 4
    assert model.winning_trades == 2
    assert model.losing_trades == 1
from reporting.models.performance_model import PerformanceModel


def test_create_performance_model():
    model = PerformanceModel()

    assert model.total_trades == 0
    assert model.winning_trades == 0
    assert model.losing_trades == 0
    assert model.net_profit == 0.0


def test_default_performance_metrics():
    model = PerformanceModel()

    assert model.gross_profit == 0.0
    assert model.gross_loss == 0.0
    assert model.win_rate == 0.0
    assert model.profit_factor == 0.0


def test_default_trade_statistics():
    model = PerformanceModel()

    assert model.average_win == 0.0
    assert model.average_loss == 0.0
    assert model.largest_win == 0.0
    assert model.largest_loss == 0.0


from reporting.models.performance_model import PerformanceModel
from reporting.services.performance_service import PerformanceService


class DummyTrade:
    def __init__(self, pnl=0.0):
        self.pnl = pnl


def test_calculate_total_trades():
    service = PerformanceService()

    trades = [
        DummyTrade(),
        DummyTrade(),
        DummyTrade(),
    ]

    model = service.calculate(trades)

    assert model.total_trades == 3

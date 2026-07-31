from reporting.services.performance_service import PerformanceService


class DummyTrade:
    def __init__(self, pnl):
        self.pnl = pnl


def test_calculate_complete_performance():
    service = PerformanceService()

    trades = [
        DummyTrade(100),
        DummyTrade(-40),
        DummyTrade(60),
        DummyTrade(-20),
    ]

    model = service.calculate(trades)

    assert model.total_trades == 4
    assert model.winning_trades == 2
    assert model.losing_trades == 2

    assert model.gross_profit == 160
    assert model.gross_loss == 60
    assert model.net_profit == 100

    assert model.win_rate == 50.0
    assert model.profit_factor == 160 / 60

    assert model.equity_curve == [100, 60, 120, 100]
    assert model.max_drawdown == 40

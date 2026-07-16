from dashboard.widgets.performance_widget import PerformanceWidget


def test_performance_widget_defaults():
    widget = PerformanceWidget()

    assert widget.win_rate == 0.0
    assert widget.total_trades == 0
    assert widget.average_profit == 0.0
    assert widget.average_loss == 0.0
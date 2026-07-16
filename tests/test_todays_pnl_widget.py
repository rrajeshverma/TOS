from dashboard.widgets.todays_pnl import TodaysPnLWidget


def test_todays_pnl_widget_defaults():
    widget = TodaysPnLWidget()

    assert widget.realized_pnl == 0.0
    assert widget.trade_count == 0
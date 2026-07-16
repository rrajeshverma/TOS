from dashboard.widgets.equity_curve import EquityCurveWidget


def test_equity_curve_widget_defaults():
    widget = EquityCurveWidget()

    assert widget.points == []
    assert widget.starting_equity == 0.0
    assert widget.current_equity == 0.0
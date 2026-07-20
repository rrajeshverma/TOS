from dashboard.widgets.unrealized_pnl import UnrealizedPnLWidget


def test_unrealized_pnl_widget_defaults():
    widget = UnrealizedPnLWidget()

    assert widget.unrealized_pnl == 0.0
    assert widget.position_count == 0

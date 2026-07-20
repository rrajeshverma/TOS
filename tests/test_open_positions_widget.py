from dashboard.widgets.open_positions import OpenPositionsWidget


def test_open_positions_widget_defaults():
    widget = OpenPositionsWidget()

    assert widget.positions == []
    assert widget.count == 0

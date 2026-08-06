from dashboard.widgets.runtime_widget import RuntimeWidget


def test_runtime_widget_defaults():
    widget = RuntimeWidget()

    assert widget.status == "STOPPED"
    assert widget.mode == "PAPER"
    assert widget.uptime == "00:00:00"


def test_runtime_widget_custom_values():
    widget = RuntimeWidget(
        status="RUNNING",
        mode="LIVE",
        uptime="01:15:42",
    )

    assert widget.status == "RUNNING"
    assert widget.mode == "LIVE"
    assert widget.uptime == "01:15:42"


def test_runtime_widget_render():
    widget = RuntimeWidget(
        status="RUNNING",
        mode="PAPER",
        uptime="00:30:00",
    )

    output = widget.render()

    assert "Runtime" in output
    assert "RUNNING" in output
    assert "PAPER" in output
    assert "00:30:00" in output

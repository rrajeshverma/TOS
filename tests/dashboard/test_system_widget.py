from dashboard.widgets.system_widget import SystemWidget


def test_system_widget_defaults():
    widget = SystemWidget()

    assert widget.cpu == 0.0
    assert widget.memory == 0.0
    assert widget.uptime == "00:00:00"


def test_system_widget_custom_values():
    widget = SystemWidget(
        cpu=6.5,
        memory=412.8,
        uptime="03:45:12",
    )

    assert widget.cpu == 6.5
    assert widget.memory == 412.8
    assert widget.uptime == "03:45:12"


def test_system_widget_render():
    widget = SystemWidget(
        cpu=4.2,
        memory=389.5,
        uptime="02:10:15",
    )

    output = widget.render()

    assert "System" in output
    assert "4.2%" in output
    assert "389.5 MB" in output
    assert "02:10:15" in output

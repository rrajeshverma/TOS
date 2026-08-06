from dashboard.widgets.alert_widget import AlertWidget


def test_alert_widget_defaults():
    widget = AlertWidget()

    assert widget.alerts == []


def test_alert_widget_with_alerts():
    widget = AlertWidget(
        [
            "Broker disconnected",
            "Daily loss limit reached",
        ]
    )

    assert len(widget.alerts) == 2


def test_alert_widget_render_empty():
    widget = AlertWidget()

    output = widget.render()

    assert "Alerts" in output
    assert "None" in output


def test_alert_widget_render_multiple():
    widget = AlertWidget(
        [
            "Broker disconnected",
            "High latency",
        ]
    )

    output = widget.render()

    assert "Broker disconnected" in output
    assert "High latency" in output

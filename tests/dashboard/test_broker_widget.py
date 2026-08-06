from dashboard.widgets.broker_widget import BrokerWidget


def test_broker_widget_defaults():
    widget = BrokerWidget()

    assert widget.connected is False
    assert widget.broker == "DHAN"
    assert widget.latency_ms == 0
    assert widget.heartbeat == "UNKNOWN"


def test_broker_widget_connected():
    widget = BrokerWidget(
        connected=True,
        broker="DHAN",
        latency_ms=38,
        heartbeat="OK",
    )

    assert widget.connected is True
    assert widget.latency_ms == 38
    assert widget.heartbeat == "OK"


def test_broker_widget_render_connected():
    widget = BrokerWidget(
        connected=True,
        broker="DHAN",
        latency_ms=42,
        heartbeat="OK",
    )

    output = widget.render()

    assert "CONNECTED" in output
    assert "42 ms" in output
    assert "OK" in output


def test_broker_widget_render_disconnected():
    widget = BrokerWidget()

    output = widget.render()

    assert "DISCONNECTED" in output

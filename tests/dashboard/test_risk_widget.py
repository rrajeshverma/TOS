from dashboard.widgets.risk_widget import RiskWidget


def test_risk_widget_defaults():
    widget = RiskWidget()

    assert widget.status == "SAFE"
    assert widget.daily_loss == 0.0
    assert widget.kill_switch is False
    assert widget.circuit_breaker is False


def test_risk_widget_custom_values():
    widget = RiskWidget(
        status="WARNING",
        daily_loss=2500,
        kill_switch=True,
        circuit_breaker=False,
    )

    assert widget.status == "WARNING"
    assert widget.daily_loss == 2500
    assert widget.kill_switch is True
    assert widget.circuit_breaker is False


def test_risk_widget_render():
    widget = RiskWidget(
        status="SAFE",
        daily_loss=1250,
        kill_switch=False,
        circuit_breaker=True,
    )

    output = widget.render()

    assert "Risk" in output
    assert "SAFE" in output
    assert "1,250.00" in output
    assert "OFF" in output
    assert "ON" in output

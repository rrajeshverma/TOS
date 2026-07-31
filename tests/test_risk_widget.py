from dashboard.widgets.risk_widget import RiskWidget


def test_risk_widget_defaults():
    widget = RiskWidget()

    assert widget.max_drawdown == 0.0
    assert widget.current_risk == 0.0
    assert widget.risk_reward_ratio == 0.0

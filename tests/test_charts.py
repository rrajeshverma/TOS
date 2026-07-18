from analytics.charts import Charts


def test_equity_curve():
    charts = Charts()

    equity = [100000, 100500, 100250, 101000]

    assert charts.equity_curve(equity) == equity


def test_drawdown_curve():
    charts = Charts()

    drawdown = [0, 0, 250, 0]

    assert charts.drawdown_curve(drawdown) == drawdown


def test_returns_curve():
    charts = Charts()

    returns = [0.01, -0.02, 0.03]

    assert charts.returns_curve(returns) == returns


def test_empty_equity_curve():
    charts = Charts()

    assert charts.equity_curve([]) == []
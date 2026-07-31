from analytics.portfolio_analytics import PortfolioAnalytics


def test_returns_dictionary():
    analytics = PortfolioAnalytics()

    metrics = analytics.calculate(
        returns=[0.01, 0.02, -0.01],
        beginning_value=100,
        ending_value=120,
        years=1,
        average_win=20,
        average_loss=10,
        net_profit=100,
        max_drawdown=20,
    )

    assert isinstance(metrics, dict)


def test_contains_all_metrics():
    analytics = PortfolioAnalytics()

    metrics = analytics.calculate(
        returns=[0.01, -0.02, 0.03],
        beginning_value=100,
        ending_value=120,
        years=1,
        average_win=20,
        average_loss=10,
        net_profit=100,
        max_drawdown=20,
    )

    expected = {
        "sharpe_ratio",
        "sortino_ratio",
        "volatility",
        "calmar_ratio",
        "cagr",
        "annual_return",
        "payoff_ratio",
        "recovery_ratio",
        "value_at_risk",
        "expected_shortfall",
    }

    assert expected == set(metrics.keys())


def test_all_values_are_float():
    analytics = PortfolioAnalytics()

    metrics = analytics.calculate(
        returns=[0.01, -0.02, 0.03],
        beginning_value=100,
        ending_value=120,
        years=1,
        average_win=20,
        average_loss=10,
        net_profit=100,
        max_drawdown=20,
    )

    for value in metrics.values():
        assert isinstance(value, float)


def test_empty_returns():
    analytics = PortfolioAnalytics()

    metrics = analytics.calculate(
        returns=[],
        beginning_value=100,
        ending_value=100,
        years=1,
        average_win=0,
        average_loss=0,
        net_profit=0,
        max_drawdown=0,
    )

    assert metrics["sharpe_ratio"] == 0.0
    assert metrics["sortino_ratio"] == 0.0
    assert metrics["volatility"] == 0.0


def test_zero_drawdown():
    analytics = PortfolioAnalytics()

    metrics = analytics.calculate(
        returns=[0.01],
        beginning_value=100,
        ending_value=120,
        years=1,
        average_win=20,
        average_loss=10,
        net_profit=100,
        max_drawdown=0,
    )

    assert metrics["calmar_ratio"] == 0.0
    assert metrics["recovery_ratio"] == 0.0


def test_zero_beginning_value():
    analytics = PortfolioAnalytics()

    metrics = analytics.calculate(
        returns=[0.01],
        beginning_value=0,
        ending_value=120,
        years=1,
        average_win=20,
        average_loss=10,
        net_profit=100,
        max_drawdown=20,
    )

    assert metrics["annual_return"] == 0.0
    assert metrics["cagr"] == 0.0


def test_positive_metrics():
    analytics = PortfolioAnalytics()

    metrics = analytics.calculate(
        returns=[0.03, 0.02, -0.01],
        beginning_value=100,
        ending_value=130,
        years=1,
        average_win=30,
        average_loss=10,
        net_profit=200,
        max_drawdown=50,
    )

    assert metrics["payoff_ratio"] > 0
    assert metrics["recovery_ratio"] > 0

from analytics.portfolio_analytics import PortfolioAnalytics


def test_empty_portfolio():
    metrics = PortfolioAnalytics().calculate(
        returns=[],
        beginning_value=100,
        ending_value=100,
        years=1,
        average_win=0,
        average_loss=0,
        net_profit=0,
        max_drawdown=0,
    )

    assert all(
        value == 0.0
        for value in metrics.values()
    )


def test_all_winning_returns():
    metrics = PortfolioAnalytics().calculate(
        returns=[0.02, 0.03, 0.01],
        beginning_value=100,
        ending_value=120,
        years=1,
        average_win=20,
        average_loss=10,
        net_profit=100,
        max_drawdown=20,
    )

    assert metrics["annual_return"] > 0
    assert metrics["payoff_ratio"] > 0


def test_all_losing_returns():
    metrics = PortfolioAnalytics().calculate(
        returns=[-0.02, -0.03, -0.01],
        beginning_value=100,
        ending_value=80,
        years=1,
        average_win=0,
        average_loss=20,
        net_profit=-20,
        max_drawdown=30,
    )

    assert metrics["annual_return"] < 0
    assert metrics["recovery_ratio"] < 0


def test_single_trade():
    metrics = PortfolioAnalytics().calculate(
        returns=[0.02],
        beginning_value=100,
        ending_value=102,
        years=1,
        average_win=2,
        average_loss=1,
        net_profit=2,
        max_drawdown=1,
    )

    assert isinstance(metrics, dict)


def test_constant_returns():
    metrics = PortfolioAnalytics().calculate(
        returns=[0.01] * 20,
        beginning_value=100,
        ending_value=120,
        years=1,
        average_win=5,
        average_loss=2,
        net_profit=20,
        max_drawdown=5,
    )

    assert metrics["volatility"] == 0.0


def test_zero_drawdown():
    metrics = PortfolioAnalytics().calculate(
        returns=[0.01, 0.02],
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
    metrics = PortfolioAnalytics().calculate(
        returns=[0.01],
        beginning_value=0,
        ending_value=100,
        years=1,
        average_win=10,
        average_loss=5,
        net_profit=10,
        max_drawdown=2,
    )

    assert metrics["annual_return"] == 0.0
    assert metrics["cagr"] == 0.0


def test_large_portfolio():
    returns = [0.01] * 500 + [-0.005] * 500

    metrics = PortfolioAnalytics().calculate(
        returns=returns,
        beginning_value=100,
        ending_value=300,
        years=5,
        average_win=10,
        average_loss=5,
        net_profit=500,
        max_drawdown=100,
    )

    assert metrics["volatility"] > 0


def test_metric_count():
    metrics = PortfolioAnalytics().calculate(
        returns=[0.01],
        beginning_value=100,
        ending_value=110,
        years=1,
        average_win=10,
        average_loss=5,
        net_profit=10,
        max_drawdown=5,
    )

    assert len(metrics) == 10


def test_metric_names():
    metrics = PortfolioAnalytics().calculate(
        returns=[0.01],
        beginning_value=100,
        ending_value=110,
        years=1,
        average_win=10,
        average_loss=5,
        net_profit=10,
        max_drawdown=5,
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

    assert set(metrics.keys()) == expected
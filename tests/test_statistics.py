from math import isclose
from analytics.statistics import Statistics


def test_win_rate_no_trades():
    stats = Statistics()

    assert stats.win_rate([]) == 0.0


def test_win_rate_all_wins():
    stats = Statistics()

    trades = [100, 200, 50]

    assert stats.win_rate(trades) == 100.0


def test_win_rate_all_losses():
    stats = Statistics()

    trades = [-100, -50, -20]

    assert stats.win_rate(trades) == 0.0


def test_win_rate_mixed():
    stats = Statistics()

    trades = [100, -50, 200, -25]

    assert stats.win_rate(trades) == 50.0

def test_average_win():
    stats = Statistics()

    trades = [100, 200, -50, 300]

    assert isclose(stats.average_win(trades), 200.0)


def test_average_loss():
    stats = Statistics()

    trades = [100, -50, -150, 300]

    assert isclose(stats.average_loss(trades), 100.0)


def test_average_win_no_wins():
    stats = Statistics()

    assert stats.average_win([-10, -20]) == 0.0


def test_average_loss_no_losses():
    stats = Statistics()

    assert stats.average_loss([10, 20]) == 0.0

def test_profit_factor():
    stats = Statistics()

    trades = [100, -50, 300, -150]

    assert isclose(stats.profit_factor(trades), 2.0)


def test_profit_factor_all_wins():
    stats = Statistics()

    trades = [100, 200, 300]

    assert stats.profit_factor(trades) == float("inf")


def test_profit_factor_all_losses():
    stats = Statistics()

    trades = [-100, -200]

    assert stats.profit_factor(trades) == 0.0


def test_profit_factor_no_trades():
    stats = Statistics()

    assert stats.profit_factor([]) == 0.0

def test_payoff_ratio():
    stats = Statistics()

    trades = [100, -50, 300, -150]

    assert isclose(stats.payoff_ratio(trades), 2.0)


def test_payoff_ratio_no_losses():
    stats = Statistics()

    trades = [100, 200]

    assert stats.payoff_ratio(trades) == float("inf")


def test_payoff_ratio_no_wins():
    stats = Statistics()

    trades = [-100, -200]

    assert stats.payoff_ratio(trades) == 0.0


def test_payoff_ratio_no_trades():
    stats = Statistics()

    assert stats.payoff_ratio([]) == 0.0


def test_expectancy_positive():
    stats = Statistics()

    trades = [100, -50, 300, -150]

    assert isclose(stats.expectancy(trades), 50.0)


def test_expectancy_all_wins():
    stats = Statistics()

    trades = [100, 200]

    assert isclose(stats.expectancy(trades), 150.0)


def test_expectancy_all_losses():
    stats = Statistics()

    trades = [-100, -200]

    assert isclose(stats.expectancy(trades), -150.0)


def test_expectancy_no_trades():
    stats = Statistics()

    assert stats.expectancy([]) == 0.0

def test_recovery_factor():
    stats = Statistics()

    assert isclose(
        stats.recovery_factor(
            net_profit=20000,
            max_drawdown=5000,
        ),
        4.0,
    )


def test_recovery_factor_zero_drawdown():
    stats = Statistics()

    assert stats.recovery_factor(
        net_profit=10000,
        max_drawdown=0,
    ) == float("inf")


def test_recovery_factor_zero_profit():
    stats = Statistics()

    assert stats.recovery_factor(
        net_profit=0,
        max_drawdown=5000,
    ) == 0.0


def test_recovery_factor_zero_profit_zero_drawdown():
    stats = Statistics()

    assert stats.recovery_factor(
        net_profit=0,
        max_drawdown=0,
    ) == 0.0

def test_sharpe_ratio():
    stats = Statistics()

    returns = [0.01, 0.02, -0.01, 0.03, 0.015]

    result = stats.sharpe_ratio(returns)

    assert result > 0


def test_sharpe_ratio_empty_returns():
    stats = Statistics()

    assert stats.sharpe_ratio([]) == 0.0


def test_sharpe_ratio_single_return():
    stats = Statistics()

    assert stats.sharpe_ratio([0.02]) == 0.0


def test_sharpe_ratio_zero_volatility():
    stats = Statistics()

    assert stats.sharpe_ratio([0.01, 0.01, 0.01]) == 0.0

def test_sortino_ratio():
    stats = Statistics()

    returns = [0.02, 0.01, -0.01, 0.03, -0.02]

    result = stats.sortino_ratio(returns)

    assert result > 0


def test_sortino_ratio_empty_returns():
    stats = Statistics()

    assert stats.sortino_ratio([]) == 0.0


def test_sortino_ratio_no_negative_returns():
    stats = Statistics()

    returns = [0.01, 0.02, 0.03]

    assert stats.sortino_ratio(returns) == 0.0


def test_sortino_ratio_single_negative_return():
    stats = Statistics()

    returns = [0.01, -0.02, 0.03]

    assert stats.sortino_ratio(returns) == 0.0

from math import isclose


def test_calmar_ratio():
    stats = Statistics()

    assert isclose(
        stats.calmar_ratio(
            cagr=20.0,
            max_drawdown_percent=10.0,
        ),
        2.0,
    )


def test_calmar_ratio_zero_drawdown():
    stats = Statistics()

    assert stats.calmar_ratio(
        cagr=20.0,
        max_drawdown_percent=0.0,
    ) == float("inf")


def test_calmar_ratio_zero_cagr():
    stats = Statistics()

    assert stats.calmar_ratio(
        cagr=0.0,
        max_drawdown_percent=10.0,
    ) == 0.0
    

def test_calmar_ratio_negative_cagr():
    stats = Statistics()

    assert isclose(
        stats.calmar_ratio(
            cagr=-10.0,
            max_drawdown_percent=5.0,
        ),
        -2.0,
    )
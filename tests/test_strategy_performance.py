from portfolio.strategy_performance import StrategyPerformance

# ============================================================
# Construction
# ============================================================


def test_initial_values():
    performance = StrategyPerformance()

    assert performance.trades == []


# ============================================================
# Add Trades
# ============================================================


def test_add_trade():
    performance = StrategyPerformance()

    performance.add_trade(100)

    assert performance.trades == [100]


def test_add_multiple_trades():
    performance = StrategyPerformance()

    performance.add_trade(100)
    performance.add_trade(-50)

    assert performance.trades == [100, -50]


# ============================================================
# Net PnL
# ============================================================


def test_net_profit():
    performance = StrategyPerformance()

    performance.add_trade(100)
    performance.add_trade(200)

    assert performance.net_profit() == 300


def test_net_loss():
    performance = StrategyPerformance()

    performance.add_trade(-100)
    performance.add_trade(-50)

    assert performance.net_profit() == -150


def test_net_mixed():
    performance = StrategyPerformance()

    performance.add_trade(200)
    performance.add_trade(-50)

    assert performance.net_profit() == 150


# ============================================================
# Win / Loss Counts
# ============================================================


def test_winning_trades():
    performance = StrategyPerformance()

    performance.add_trade(100)
    performance.add_trade(-50)
    performance.add_trade(200)

    assert performance.winning_trades() == 2


def test_losing_trades():
    performance = StrategyPerformance()

    performance.add_trade(100)
    performance.add_trade(-50)
    performance.add_trade(-25)

    assert performance.losing_trades() == 2


def test_total_trades():
    performance = StrategyPerformance()

    performance.add_trade(1)
    performance.add_trade(2)
    performance.add_trade(3)

    assert performance.total_trades() == 3


# ============================================================
# Win Rate
# ============================================================


def test_win_rate():
    performance = StrategyPerformance()

    performance.add_trade(100)
    performance.add_trade(200)
    performance.add_trade(-100)
    performance.add_trade(-50)

    assert performance.win_rate() == 50.0


def test_win_rate_zero():
    performance = StrategyPerformance()

    assert performance.win_rate() == 0.0


# ============================================================
# Largest Trades
# ============================================================


def test_largest_win():
    performance = StrategyPerformance()

    performance.add_trade(100)
    performance.add_trade(250)
    performance.add_trade(150)

    assert performance.largest_win() == 250


def test_largest_loss():
    performance = StrategyPerformance()

    performance.add_trade(-100)
    performance.add_trade(-250)
    performance.add_trade(-150)

    assert performance.largest_loss() == -250


# ============================================================
# Summary
# ============================================================


def test_summary_net_profit():
    performance = StrategyPerformance()

    performance.add_trade(100)

    assert performance.summary()["net_profit"] == 100


def test_summary_total_trades():
    performance = StrategyPerformance()

    performance.add_trade(100)

    assert performance.summary()["total_trades"] == 1


def test_summary_win_rate():
    performance = StrategyPerformance()

    performance.add_trade(100)

    assert performance.summary()["win_rate"] == 100.0


def test_summary_winners():
    performance = StrategyPerformance()

    performance.add_trade(100)

    assert performance.summary()["winning_trades"] == 1


def test_summary_losers():
    performance = StrategyPerformance()

    performance.add_trade(-100)

    assert performance.summary()["losing_trades"] == 1


def test_summary_largest_win():
    performance = StrategyPerformance()

    performance.add_trade(200)

    assert performance.summary()["largest_win"] == 200


def test_summary_largest_loss():
    performance = StrategyPerformance()

    performance.add_trade(-300)

    assert performance.summary()["largest_loss"] == -300


# ============================================================
# Gross Profit / Loss
# ============================================================


def test_gross_profit():
    performance = StrategyPerformance()

    performance.add_trade(100)
    performance.add_trade(-50)
    performance.add_trade(200)

    assert performance.gross_profit() == 300


def test_gross_loss():
    performance = StrategyPerformance()

    performance.add_trade(100)
    performance.add_trade(-50)
    performance.add_trade(-150)

    assert performance.gross_loss() == 200


# ============================================================
# Average Win / Loss
# ============================================================


def test_average_win():
    performance = StrategyPerformance()

    performance.add_trade(100)
    performance.add_trade(300)

    assert performance.average_win() == 200


def test_average_loss():
    performance = StrategyPerformance()

    performance.add_trade(-100)
    performance.add_trade(-300)

    assert performance.average_loss() == 200


# ============================================================
# Profit Factor
# ============================================================


def test_profit_factor():
    performance = StrategyPerformance()

    performance.add_trade(200)
    performance.add_trade(-100)

    assert performance.profit_factor() == 2.0


def test_profit_factor_zero_loss():
    performance = StrategyPerformance()

    performance.add_trade(200)

    assert performance.profit_factor() == float("inf")


# ============================================================
# Expectancy
# ============================================================


def test_expectancy():
    performance = StrategyPerformance()

    performance.add_trade(100)
    performance.add_trade(-50)

    assert performance.expectancy() == 25


# ============================================================
# Consecutive Wins
# ============================================================


def test_max_consecutive_wins():
    performance = StrategyPerformance()

    performance.add_trade(10)
    performance.add_trade(20)
    performance.add_trade(-5)
    performance.add_trade(30)
    performance.add_trade(40)
    performance.add_trade(50)

    assert performance.max_consecutive_wins() == 3


# ============================================================
# Consecutive Losses
# ============================================================


def test_max_consecutive_losses():
    performance = StrategyPerformance()

    performance.add_trade(-10)
    performance.add_trade(-20)
    performance.add_trade(5)
    performance.add_trade(-30)
    performance.add_trade(-40)
    performance.add_trade(-50)

    assert performance.max_consecutive_losses() == 3


# ============================================================
# Average Trade
# ============================================================


def test_average_trade():
    performance = StrategyPerformance()

    performance.add_trade(100)
    performance.add_trade(-50)
    performance.add_trade(150)

    assert performance.average_trade() == 200 / 3


# ============================================================
# Payoff Ratio
# ============================================================


def test_payoff_ratio():
    performance = StrategyPerformance()

    performance.add_trade(200)
    performance.add_trade(-100)

    assert performance.payoff_ratio() == 2.0


def test_payoff_ratio_zero_losses():
    performance = StrategyPerformance()

    performance.add_trade(100)

    assert performance.payoff_ratio() == float("inf")


# ============================================================
# Running Equity
# ============================================================


def test_running_equity():
    performance = StrategyPerformance()

    performance.add_trade(100)
    performance.add_trade(-50)

    assert performance.running_equity(1000) == [1000, 1100, 1050]


# ============================================================
# Equity High
# ============================================================


def test_equity_high():
    performance = StrategyPerformance()

    performance.add_trade(100)
    performance.add_trade(-50)
    performance.add_trade(200)

    assert performance.equity_high(1000) == 1250


# ============================================================
# Summary Extensions
# ============================================================


def test_summary_average_trade():
    performance = StrategyPerformance()

    performance.add_trade(100)

    assert performance.summary()["average_trade"] == 100


def test_summary_payoff_ratio():
    performance = StrategyPerformance()

    performance.add_trade(100)

    assert performance.summary()["payoff_ratio"] == float("inf")


def test_summary_gross_profit():
    performance = StrategyPerformance()

    performance.add_trade(100)

    assert performance.summary()["gross_profit"] == 100


def test_summary_gross_loss():
    performance = StrategyPerformance()

    performance.add_trade(-100)

    assert performance.summary()["gross_loss"] == 100


def test_summary_expectancy():
    performance = StrategyPerformance()

    performance.add_trade(100)
    performance.add_trade(-50)

    assert performance.summary()["expectancy"] == 25


# ============================================================
# Guard Clauses
# ============================================================


def test_largest_win_no_winners():
    performance = StrategyPerformance()

    assert performance.largest_win() == 0


def test_largest_loss_no_losers():
    performance = StrategyPerformance()

    assert performance.largest_loss() == 0


def test_average_win_no_winners():
    performance = StrategyPerformance()

    assert performance.average_win() == 0


def test_average_loss_no_losers():
    performance = StrategyPerformance()

    assert performance.average_loss() == 0


def test_expectancy_no_trades():
    performance = StrategyPerformance()

    assert performance.expectancy() == 0


def test_average_trade_no_trades():
    performance = StrategyPerformance()

    assert performance.average_trade() == 0


def test_payoff_ratio_no_losses():
    performance = StrategyPerformance()

    performance.add_trade(100)

    assert performance.payoff_ratio() == float("inf")


def test_running_equity():
    performance = StrategyPerformance()

    performance.add_trade(100)
    performance.add_trade(-50)

    assert performance.running_equity(1000) == [1000, 1100, 1050]


def test_equity_high():
    performance = StrategyPerformance()

    performance.add_trade(100)
    performance.add_trade(-50)
    performance.add_trade(200)

    assert performance.equity_high(1000) == 1250

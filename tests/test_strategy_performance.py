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
from reporting.reports.statistics import Statistics


def test_win_rate_all_wins():
    stats = Statistics()

    assert stats.win_rate(10, 10) == 100.0


def test_win_rate_half():
    stats = Statistics()

    assert stats.win_rate(5, 10) == 50.0


def test_win_rate_zero_trades():
    stats = Statistics()

    assert stats.win_rate(0, 0) == 0.0


def test_profit_factor():
    stats = Statistics()

    assert stats.profit_factor(1000, 500) == 2.0


def test_profit_factor_zero_loss():
    stats = Statistics()

    assert stats.profit_factor(1000, 0) == 0.0


def test_average_win():
    stats = Statistics()

    assert stats.average_win(1000, 4) == 250.0


def test_average_win_zero():
    stats = Statistics()

    assert stats.average_win(1000, 0) == 0.0


def test_average_loss():
    stats = Statistics()

    assert stats.average_loss(500, 2) == 250.0


def test_average_loss_zero():
    stats = Statistics()

    assert stats.average_loss(500, 0) == 0.0


def test_expectancy_positive():
    stats = Statistics()

    result = stats.expectancy(
        average_win=200,
        average_loss=100,
        win_rate=60,
    )

    assert result == 80.0


def test_expectancy_negative():
    stats = Statistics()

    result = stats.expectancy(
        average_win=100,
        average_loss=200,
        win_rate=40,
    )

    assert result == -80.0


def test_expectancy_break_even():
    stats = Statistics()

    result = stats.expectancy(
        average_win=100,
        average_loss=100,
        win_rate=50,
    )

    assert result == 0.0
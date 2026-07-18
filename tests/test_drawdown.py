from analytics.drawdown import Drawdown


def test_no_drawdown_at_start():
    dd = Drawdown()

    assert dd.calculate(100000, 100000) == 0


def test_simple_drawdown():
    dd = Drawdown()

    assert dd.calculate(95000, 100000) == 5000


def test_drawdown_percentage():
    dd = Drawdown()

    assert dd.calculate_percentage(95000, 100000) == 5.0


def test_zero_drawdown_after_new_high():
    dd = Drawdown()

    assert dd.calculate(105000, 105000) == 0

from analytics.drawdown import Drawdown


def test_max_drawdown_initially_zero():
    dd = Drawdown()

    assert dd.max_drawdown == 0


def test_max_drawdown_updates():
    dd = Drawdown()

    dd.update(100000, 100000)
    dd.update(98000, 100000)

    assert dd.max_drawdown == 2000


def test_max_drawdown_keeps_largest_loss():
    dd = Drawdown()

    dd.update(100000, 100000)
    dd.update(98000, 100000)
    dd.update(99000, 100000)
    dd.update(95000, 100000)

    assert dd.max_drawdown == 5000


def test_max_drawdown_not_reduced_after_recovery():
    dd = Drawdown()

    dd.update(100000, 100000)
    dd.update(95000, 100000)
    dd.update(100000, 100000)

    assert dd.max_drawdown == 5000

from analytics.drawdown import Drawdown


def test_drawdown_duration_starts_at_zero():
    dd = Drawdown()

    assert dd.duration == 0


def test_drawdown_duration_increases():
    dd = Drawdown()

    dd.update(99000, 100000)
    dd.update(98000, 100000)

    assert dd.duration == 2


def test_drawdown_duration_resets_after_recovery():
    dd = Drawdown()

    dd.update(99000, 100000)
    dd.update(98000, 100000)
    dd.update(100000, 100000)

    assert dd.duration == 0


def test_max_drawdown_duration():
    dd = Drawdown()

    dd.update(99000, 100000)
    dd.update(98000, 100000)
    dd.update(97000, 100000)
    dd.update(100000, 100000)

    assert dd.max_duration == 3
from analytics.performance_metrics import PerformanceMetrics


def test_total_return():
    assert PerformanceMetrics.total_return([100, -50, 25]) == 75


def test_total_return_empty():
    assert PerformanceMetrics.total_return([]) == 0


def test_average_trade():
    assert PerformanceMetrics.average_trade([100, -50, 25]) == 25


def test_average_trade_empty():
    assert PerformanceMetrics.average_trade([]) == 0


def test_best_trade():
    assert PerformanceMetrics.best_trade([100, 250, -25]) == 250


def test_best_trade_empty():
    assert PerformanceMetrics.best_trade([]) == 0


def test_worst_trade():
    assert PerformanceMetrics.worst_trade([100, -250, 50]) == -250


def test_worst_trade_empty():
    assert PerformanceMetrics.worst_trade([]) == 0


def test_positive_trade_count():
    assert PerformanceMetrics.positive_trade_count([100, -50, 25]) == 2


def test_negative_trade_count():
    assert PerformanceMetrics.negative_trade_count([100, -50, 25]) == 1


def test_win_rate():
    assert PerformanceMetrics.win_rate([100, -50, 25, -10]) == 50.0


def test_win_rate_empty():
    assert PerformanceMetrics.win_rate([]) == 0


def test_class_exists():
    assert PerformanceMetrics is not None


def test_zero_trade():
    assert PerformanceMetrics.total_return([0]) == 0


def test_single_trade():
    assert PerformanceMetrics.average_trade([150]) == 150

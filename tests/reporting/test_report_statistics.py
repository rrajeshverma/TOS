from reporting.report_statistics import ReportStatistics


def test_trade_count():
    assert ReportStatistics.trade_count([1, 2, 3]) == 3


def test_trade_count_empty():
    assert ReportStatistics.trade_count([]) == 0


def test_total_profit():
    assert ReportStatistics.total_profit([100, 200, -50]) == 250


def test_total_profit_empty():
    assert ReportStatistics.total_profit([]) == 0


def test_average_profit():
    assert ReportStatistics.average_profit([100, 200, 300]) == 200


def test_average_profit_empty():
    assert ReportStatistics.average_profit([]) == 0


def test_best_trade():
    assert ReportStatistics.best_trade([100, 500, 200]) == 500


def test_best_trade_empty():
    assert ReportStatistics.best_trade([]) == 0


def test_worst_trade():
    assert ReportStatistics.worst_trade([100, -250, 300]) == -250


def test_worst_trade_empty():
    assert ReportStatistics.worst_trade([]) == 0


def test_win_count():
    assert ReportStatistics.win_count([100, -50, 25]) == 2


def test_loss_count():
    assert ReportStatistics.loss_count([100, -50, 25]) == 1


def test_win_rate():
    assert ReportStatistics.win_rate([100, -50, 25, -10]) == 50.0


def test_win_rate_empty():
    assert ReportStatistics.win_rate([]) == 0


def test_class_exists():
    assert ReportStatistics is not None

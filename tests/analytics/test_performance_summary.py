from analytics.performance_summary import PerformanceSummary


def test_summary_creation():
    summary = PerformanceSummary()
    assert summary is not None


def test_generate_returns_dict():
    summary = PerformanceSummary()

    result = summary.generate([100, -50, 25])

    assert isinstance(result, dict)


def test_contains_total_return():
    result = PerformanceSummary().generate([100, -50, 25])

    assert "total_return" in result


def test_contains_average_trade():
    result = PerformanceSummary().generate([100, -50, 25])

    assert "average_trade" in result


def test_contains_best_trade():
    result = PerformanceSummary().generate([100, -50, 25])

    assert "best_trade" in result


def test_contains_worst_trade():
    result = PerformanceSummary().generate([100, -50, 25])

    assert "worst_trade" in result


def test_contains_win_rate():
    result = PerformanceSummary().generate([100, -50, 25])

    assert "win_rate" in result


def test_total_return_value():
    result = PerformanceSummary().generate([100, -50, 25])

    assert result["total_return"] == 75


def test_average_trade_value():
    result = PerformanceSummary().generate([100, -50, 25])

    assert result["average_trade"] == 25


def test_best_trade_value():
    result = PerformanceSummary().generate([100, -50, 25])

    assert result["best_trade"] == 100


def test_worst_trade_value():
    result = PerformanceSummary().generate([100, -50, 25])

    assert result["worst_trade"] == -50


def test_empty_list():
    result = PerformanceSummary().generate([])

    assert result["total_return"] == 0


def test_single_trade():
    result = PerformanceSummary().generate([200])

    assert result["total_return"] == 200


def test_repeatable():
    summary = PerformanceSummary()

    assert summary.generate([10]) == summary.generate([10])


def test_class_exists():
    assert PerformanceSummary is not None
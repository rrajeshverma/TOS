from reporting.report_model import ReportModel


def test_add_trade_count():
    report = ReportModel("Daily", __import__("datetime").datetime.now())

    report.summary["total_trades"] = 25

    assert report.summary["total_trades"] == 25


def test_add_winning_trades():
    report = ReportModel("Daily", __import__("datetime").datetime.now())

    report.summary["winning_trades"] = 18

    assert report.summary["winning_trades"] == 18


def test_add_losing_trades():
    report = ReportModel("Daily", __import__("datetime").datetime.now())

    report.summary["losing_trades"] = 7

    assert report.summary["losing_trades"] == 7


def test_add_win_rate():
    report = ReportModel("Daily", __import__("datetime").datetime.now())

    report.summary["win_rate"] = 72.0

    assert report.summary["win_rate"] == 72.0


def test_add_net_pnl():
    report = ReportModel("Daily", __import__("datetime").datetime.now())

    report.summary["net_pnl"] = 12500

    assert report.summary["net_pnl"] == 12500


def test_add_profit_factor():
    report = ReportModel("Daily", __import__("datetime").datetime.now())

    report.summary["profit_factor"] = 1.8

    assert report.summary["profit_factor"] == 1.8


def test_add_max_drawdown():
    report = ReportModel("Daily", __import__("datetime").datetime.now())

    report.summary["max_drawdown"] = 3500

    assert report.summary["max_drawdown"] == 3500


def test_add_expectancy():
    report = ReportModel("Daily", __import__("datetime").datetime.now())

    report.summary["expectancy"] = 250

    assert report.summary["expectancy"] == 250


def test_add_average_win():
    report = ReportModel("Daily", __import__("datetime").datetime.now())

    report.summary["average_win"] = 900

    assert report.summary["average_win"] == 900


def test_add_average_loss():
    report = ReportModel("Daily", __import__("datetime").datetime.now())

    report.summary["average_loss"] = 500

    assert report.summary["average_loss"] == 500


def test_summary_is_dictionary():
    report = ReportModel("Daily", __import__("datetime").datetime.now())

    assert isinstance(report.summary, dict)


def test_summary_can_store_multiple_metrics():
    report = ReportModel("Daily", __import__("datetime").datetime.now())

    report.summary["a"] = 1
    report.summary["b"] = 2

    assert len(report.summary) == 2


def test_summary_keys_are_strings():
    report = ReportModel("Daily", __import__("datetime").datetime.now())

    report.summary["metric"] = 1

    assert "metric" in report.summary


def test_summary_values_can_be_numeric():
    report = ReportModel("Daily", __import__("datetime").datetime.now())

    report.summary["value"] = 10.5

    assert isinstance(report.summary["value"], float)


def test_summary_defaults_empty():
    report = ReportModel("Daily", __import__("datetime").datetime.now())

    assert len(report.summary) == 0
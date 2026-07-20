from reporting.models.performance_model import PerformanceModel
from reporting.reports.performance_report import PerformanceReport
from reporting.reports.report_generator import ReportGenerator


# ---------------------------------------------------------------------
# PerformanceReport
# ---------------------------------------------------------------------

def test_has_summary():
    report = PerformanceReport(
        performance=PerformanceModel(),
        summary="Hello",
    )

    assert report.has_summary()


def test_is_empty():
    report = PerformanceReport(
        performance=PerformanceModel(),
    )

    assert report.is_empty()


def test_update_summary():
    report = PerformanceReport(
        performance=PerformanceModel(),
    )

    report.update_summary("ABC")

    assert report.summary == "ABC"


def test_append_summary():
    report = PerformanceReport(
        performance=PerformanceModel(),
        summary="ABC",
    )

    report.append_summary("DEF")

    assert report.summary == "ABCDEF"


def test_clear_summary():
    report = PerformanceReport(
        performance=PerformanceModel(),
        summary="ABC",
    )

    report.clear_summary()

    assert report.summary == ""


def test_summary_length():
    report = PerformanceReport(
        performance=PerformanceModel(),
        summary="ABCDE",
    )

    assert report.summary_length() == 5


def test_report_name():
    report = PerformanceReport(
        performance=PerformanceModel(),
    )

    assert report.report_name() == "Performance Report"


def test_copy():
    report = PerformanceReport(
        performance=PerformanceModel(),
        summary="Summary",
    )

    copied = report.copy()

    assert copied.summary == report.summary
    assert copied.performance == report.performance
    assert copied is not report


def test_to_dict():
    report = PerformanceReport(
        performance=PerformanceModel(),
        summary="Summary",
    )

    data = report.to_dict()

    assert data["summary"] == "Summary"
    assert isinstance(data["performance"], PerformanceModel)


# ---------------------------------------------------------------------
# ReportGenerator
# ---------------------------------------------------------------------

def test_generate_returns_report():
    performance = PerformanceModel()

    report = ReportGenerator().generate(performance)

    assert isinstance(report, PerformanceReport)


def test_generate_keeps_performance():
    performance = PerformanceModel()

    report = ReportGenerator().generate(performance)

    assert report.performance is performance


def test_generate_contains_total_trades():
    performance = PerformanceModel(total_trades=15)

    report = ReportGenerator().generate(performance)

    assert "Total Trades: 15" in report.summary


def test_generate_contains_winning_trades():
    performance = PerformanceModel(winning_trades=8)

    report = ReportGenerator().generate(performance)

    assert "Winning Trades: 8" in report.summary


def test_generate_contains_losing_trades():
    performance = PerformanceModel(losing_trades=7)

    report = ReportGenerator().generate(performance)

    assert "Losing Trades: 7" in report.summary


def test_generate_contains_net_profit():
    performance = PerformanceModel(net_profit=1500)

    report = ReportGenerator().generate(performance)

    assert "Net Profit: 1500" in report.summary


def test_generate_contains_profit_factor():
    performance = PerformanceModel(profit_factor=2.45)

    report = ReportGenerator().generate(performance)

    assert "Profit Factor: 2.45" in report.summary


def test_generate_contains_drawdown():
    performance = PerformanceModel(max_drawdown=325)

    report = ReportGenerator().generate(performance)

    assert "Maximum Drawdown: 325" in report.summary


def test_generate_contains_streaks():
    performance = PerformanceModel(
        max_consecutive_wins=5,
        max_consecutive_losses=3,
    )

    report = ReportGenerator().generate(performance)

    assert "Maximum Consecutive Wins: 5" in report.summary
    assert "Maximum Consecutive Losses: 3" in report.summary


def test_generate_summary_not_empty():
    performance = PerformanceModel()

    report = ReportGenerator().generate(performance)

    assert report.has_summary()
from reporting.report_builder import ReportBuilder
from reporting.html_report import HTMLReport
from analytics.performance_summary import PerformanceSummary
from journal.trade_journal import TradeJournal
from monitoring.health_check import HealthCheck


def test_trading_day_report_created():
    report = ReportBuilder().build(
        "Trading Day",
        [100, -50, 25],
    )

    assert report.title == "Trading Day"


def test_summary_generated():
    summary = PerformanceSummary().generate(
        [100, -50, 25],
    )

    assert summary["total_return"] == 75


def test_html_generated():
    report = ReportBuilder().build(
        "Trading Day",
        [100, -50, 25],
    )

    html = HTMLReport().render(report)

    assert "<html>" in html


def test_html_contains_title():
    report = ReportBuilder().build(
        "Trading Day",
        [100],
    )

    html = HTMLReport().render(report)

    assert "Trading Day" in html


def test_html_contains_table():
    report = ReportBuilder().build(
        "Trading Day",
        [100],
    )

    html = HTMLReport().render(report)

    assert "<table>" in html


def test_trade_journal_exists():
    assert TradeJournal() is not None


def test_health_check_exists():
    assert HealthCheck() is not None


def test_empty_trades():
    report = ReportBuilder().build(
        "Empty",
        [],
    )

    html = HTMLReport().render(report)

    assert "total_trades" in html


def test_single_trade():
    summary = PerformanceSummary().generate([250])

    assert summary["total_return"] == 250


def test_negative_trade():
    summary = PerformanceSummary().generate([-100])

    assert summary["total_return"] == -100


def test_repeatable_summary():
    ps = PerformanceSummary()

    assert ps.generate([10]) == ps.generate([10])


def test_repeatable_report():
    builder = ReportBuilder()

    report = builder.build("Day", [10])

    renderer = HTMLReport()

    assert renderer.render(report) == renderer.render(report)


def test_html_not_empty():
    report = ReportBuilder().build(
        "Day",
        [10],
    )

    assert HTMLReport().render(report)


def test_summary_is_dict():
    assert isinstance(
        PerformanceSummary().generate([1]),
        dict,
    )


def test_pipeline_complete():
    report = ReportBuilder().build(
        "Trading Day",
        [100, -50, 25],
    )

    html = HTMLReport().render(report)

    assert html.startswith("<html>")
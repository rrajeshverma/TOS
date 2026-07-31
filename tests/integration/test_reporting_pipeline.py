from analytics.performance_summary import PerformanceSummary
from reporting.html_report import HTMLReport
from reporting.report_builder import ReportBuilder


def test_pipeline_generates_report():
    builder = ReportBuilder()

    report = builder.build("Daily Report", [100, -50, 25])

    assert report.title == "Daily Report"


def test_pipeline_generates_html():
    report = ReportBuilder().build(
        "Daily Report",
        [100, -50, 25],
    )

    html = HTMLReport().render(report)

    assert "<html>" in html


def test_pipeline_contains_title():
    report = ReportBuilder().build(
        "Daily Report",
        [100, -50, 25],
    )

    html = HTMLReport().render(report)

    assert "Daily Report" in html


def test_pipeline_contains_total_trades():
    report = ReportBuilder().build(
        "Daily Report",
        [100, -50, 25],
    )

    html = HTMLReport().render(report)

    assert "total_trades" in html


def test_pipeline_contains_total_profit():
    report = ReportBuilder().build(
        "Daily Report",
        [100, -50, 25],
    )

    html = HTMLReport().render(report)

    assert "total_profit" in html


def test_pipeline_contains_table():
    report = ReportBuilder().build(
        "Daily Report",
        [100, -50, 25],
    )

    html = HTMLReport().render(report)

    assert "<table>" in html


def test_performance_summary_returns_dict():
    summary = PerformanceSummary().generate([100, -50, 25])

    assert isinstance(summary, dict)


def test_summary_contains_total_return():
    summary = PerformanceSummary().generate([100, -50, 25])

    assert "total_return" in summary


def test_summary_contains_win_rate():
    summary = PerformanceSummary().generate([100, -50, 25])

    assert "win_rate" in summary


def test_pipeline_empty_trade_list():
    report = ReportBuilder().build(
        "Empty",
        [],
    )

    html = HTMLReport().render(report)

    assert "total_trades" in html


def test_pipeline_single_trade():
    report = ReportBuilder().build(
        "Single",
        [100],
    )

    html = HTMLReport().render(report)

    assert "100" in html


def test_pipeline_repeatable():
    builder = ReportBuilder()

    report = builder.build(
        "Daily",
        [100],
    )

    renderer = HTMLReport()

    assert renderer.render(report) == renderer.render(report)


def test_pipeline_export(tmp_path):
    renderer = HTMLReport()

    report = ReportBuilder().build(
        "Export",
        [100],
    )

    output = tmp_path / "report.html"

    renderer.export(report, output)

    assert output.exists()


def test_pipeline_html_is_string():
    report = ReportBuilder().build(
        "Daily",
        [100],
    )

    assert isinstance(
        HTMLReport().render(report),
        str,
    )


def test_pipeline_html_not_empty():
    report = ReportBuilder().build(
        "Daily",
        [100],
    )

    assert HTMLReport().render(report)

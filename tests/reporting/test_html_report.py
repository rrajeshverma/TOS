from datetime import datetime

from reporting.html_report import HTMLReport
from reporting.report_model import ReportModel


def make_report():
    return ReportModel(
        title="Daily Report",
        generated_at=datetime(2026, 7, 21, 10, 0),
        summary={"trades": 10},
        sections=["Performance"],
        metadata={"version": "1.0"},
    )


def test_html_report_creation():
    renderer = HTMLReport()
    assert renderer is not None


def test_render_returns_string():
    renderer = HTMLReport()
    assert isinstance(renderer.render(make_report()), str)


def test_render_contains_html_tag():
    renderer = HTMLReport()
    assert "<html>" in renderer.render(make_report())


def test_render_contains_body():
    renderer = HTMLReport()
    assert "<body>" in renderer.render(make_report())


def test_render_contains_title():
    renderer = HTMLReport()
    assert "Daily Report" in renderer.render(make_report())


def test_render_contains_summary():
    renderer = HTMLReport()
    assert "trades" in renderer.render(make_report())


def test_render_contains_sections():
    renderer = HTMLReport()
    assert "Performance" in renderer.render(make_report())


def test_render_contains_metadata():
    renderer = HTMLReport()
    assert "version" in renderer.render(make_report())


def test_render_closes_html():
    renderer = HTMLReport()
    html = renderer.render(make_report())
    assert "</html>" in html


def test_render_closes_body():
    renderer = HTMLReport()
    html = renderer.render(make_report())
    assert "</body>" in html


def test_renderer_repr():
    assert "HTMLReport" in repr(HTMLReport())


def test_multiple_renders():
    renderer = HTMLReport()
    assert renderer.render(make_report()) == renderer.render(make_report())


def test_render_returns_non_empty():
    renderer = HTMLReport()
    assert renderer.render(make_report())


def test_render_type():
    renderer = HTMLReport()
    assert type(renderer.render(make_report())) is str


def test_html_report_instance():
    assert isinstance(HTMLReport(), HTMLReport)

from reporting.report_builder import ReportBuilder
from reporting.html_report import HTMLReport


def make_statistics_report():
    return ReportBuilder().build(
        "Daily",
        [100, -50, 25],
    )


def test_summary_table_exists():
    html = HTMLReport().render(make_statistics_report())
    assert "<table>" in html


def make_statistics_report():
    report = ReportBuilder().build(
        "Daily Report",
        [100, -50, 25],
    )

    report.sections.append("Performance")
    report.metadata["version"] = "1.0"

    return report
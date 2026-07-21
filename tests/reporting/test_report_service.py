from datetime import datetime

from reporting.report_model import ReportModel
from reporting.report_service import ReportService
from reporting.report_template import ReportTemplate


def test_service_creation():
    service = ReportService()

    assert service is not None


def test_generate_report_returns_report_model():
    service = ReportService()

    report = service.generate("Daily Report")

    assert isinstance(report, ReportModel)


def test_generated_report_title():
    service = ReportService()

    report = service.generate("Performance")

    assert report.title == "Performance"


def test_generated_report_has_timestamp():
    service = ReportService()

    report = service.generate("Daily")

    assert isinstance(report.generated_at, datetime)


def test_generated_report_default_summary():
    service = ReportService()

    report = service.generate("Daily")

    assert report.summary == {}


def test_generated_report_default_sections():
    service = ReportService()

    report = service.generate("Daily")

    assert report.sections == []


def test_generated_report_default_metadata():
    service = ReportService()

    report = service.generate("Daily")

    assert report.metadata == {}


def test_generate_with_summary():
    service = ReportService()

    report = service.generate(
        "Daily",
        summary={"trades": 10},
    )

    assert report.summary["trades"] == 10


def test_generate_with_sections():
    service = ReportService()

    report = service.generate(
        "Daily",
        sections=["Performance"],
    )

    assert report.sections == ["Performance"]


def test_generate_with_metadata():
    service = ReportService()

    report = service.generate(
        "Daily",
        metadata={"version": "1.0"},
    )

    assert report.metadata["version"] == "1.0"


def test_service_multiple_reports():
    service = ReportService()

    first = service.generate("One")
    second = service.generate("Two")

    assert first.title == "One"
    assert second.title == "Two"


def test_service_uses_template():
    template = ReportTemplate(name="default")

    service = ReportService(template)

    assert service.template == template


def test_service_repr():
    service = ReportService()

    assert "ReportService" in repr(service)


def test_service_has_template_attribute():
    service = ReportService()

    assert hasattr(service, "template")


def test_service_generate_returns_new_instance():
    service = ReportService()

    first = service.generate("A")
    second = service.generate("A")

    assert first is not second

from reporting.html_report import HTMLReport


def test_render_report_returns_html():
    service = ReportService()

    report = service.generate("Daily")

    renderer = HTMLReport()

    html = renderer.render(report)

    assert isinstance(html, str)


def test_generated_html_contains_title():
    service = ReportService()

    report = service.generate("Daily Report")

    html = HTMLReport().render(report)

    assert "Daily Report" in html


def test_generated_html_contains_html_tag():
    service = ReportService()

    report = service.generate("Daily")

    html = HTMLReport().render(report)

    assert "<html>" in html


def test_generated_html_contains_body():
    service = ReportService()

    report = service.generate("Daily")

    html = HTMLReport().render(report)

    assert "<body>" in html


def test_generate_summary_visible_in_html():
    service = ReportService()

    report = service.generate(
        "Daily",
        summary={"Trades": 12},
    )

    html = HTMLReport().render(report)

    assert "Trades" in html


def test_generate_sections_visible_in_html():
    service = ReportService()

    report = service.generate(
        "Daily",
        sections=["Performance"],
    )

    html = HTMLReport().render(report)

    assert "Performance" in html


def test_generate_metadata_visible_in_html():
    service = ReportService()

    report = service.generate(
        "Daily",
        metadata={"Version": "1.0"},
    )

    html = HTMLReport().render(report)

    assert "Version" in html


def test_render_multiple_reports():
    service = ReportService()

    html1 = HTMLReport().render(service.generate("One"))
    html2 = HTMLReport().render(service.generate("Two"))

    assert html1 != html2


def test_render_empty_report():
    service = ReportService()

    html = HTMLReport().render(service.generate(""))

    assert isinstance(html, str)


def test_html_report_is_repeatable():
    service = ReportService()

    report = service.generate("Daily")

    renderer = HTMLReport()

    assert renderer.render(report) == renderer.render(report)
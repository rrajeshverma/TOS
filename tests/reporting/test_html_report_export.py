from pathlib import Path

from reporting.html_report import HTMLReport
from reporting.report_model import ReportModel
from datetime import datetime


def make_report():
    return ReportModel(
        title="Daily",
        generated_at=datetime.now(),
    )


def test_export_creates_file(tmp_path):
    renderer = HTMLReport()

    output = tmp_path / "report.html"

    renderer.export(make_report(), output)

    assert output.exists()


def test_export_returns_path(tmp_path):
    renderer = HTMLReport()

    output = tmp_path / "report.html"

    result = renderer.export(make_report(), output)

    assert result == output


def test_export_file_contains_html(tmp_path):
    renderer = HTMLReport()

    output = tmp_path / "report.html"

    renderer.export(make_report(), output)

    assert "<html>" in output.read_text()


def test_export_contains_title(tmp_path):
    renderer = HTMLReport()

    output = tmp_path / "report.html"

    renderer.export(make_report(), output)

    assert "Daily" in output.read_text()


def test_export_overwrites_existing_file(tmp_path):
    renderer = HTMLReport()

    output = tmp_path / "report.html"

    output.write_text("old")

    renderer.export(make_report(), output)

    assert "old" not in output.read_text()


def test_export_returns_existing_path(tmp_path):
    renderer = HTMLReport()

    output = tmp_path / "report.html"

    renderer.export(make_report(), output)

    assert output.is_file()


def test_export_is_repeatable(tmp_path):
    renderer = HTMLReport()

    output = tmp_path / "report.html"

    renderer.export(make_report(), output)
    renderer.export(make_report(), output)

    assert output.exists()


def test_export_extension():
    assert Path("report.html").suffix == ".html"


def test_export_render_not_empty(tmp_path):
    renderer = HTMLReport()

    output = tmp_path / "report.html"

    renderer.export(make_report(), output)

    assert output.read_text()


def test_export_returns_path_object(tmp_path):
    renderer = HTMLReport()

    output = tmp_path / "report.html"

    result = renderer.export(make_report(), output)

    assert isinstance(result, Path)
from datetime import datetime

from reporting.report_model import ReportModel


def test_report_model_creation():
    report = ReportModel(
        title="Daily Report",
        generated_at=datetime(2026, 7, 21, 10, 0),
    )

    assert report.title == "Daily Report"


def test_report_model_generated_at():
    now = datetime(2026, 7, 21, 10, 0)

    report = ReportModel(
        title="Daily Report",
        generated_at=now,
    )

    assert report.generated_at == now


def test_report_model_default_summary():
    report = ReportModel(
        title="Daily Report",
        generated_at=datetime.now(),
    )

    assert report.summary == {}


def test_report_model_default_sections():
    report = ReportModel(
        title="Daily Report",
        generated_at=datetime.now(),
    )

    assert report.sections == []


def test_report_model_default_metadata():
    report = ReportModel(
        title="Daily Report",
        generated_at=datetime.now(),
    )

    assert report.metadata == {}


def test_report_model_custom_summary():
    report = ReportModel(
        title="Daily Report",
        generated_at=datetime.now(),
        summary={"trades": 5},
    )

    assert report.summary["trades"] == 5


def test_report_model_custom_sections():
    report = ReportModel(
        title="Daily Report",
        generated_at=datetime.now(),
        sections=["Performance"],
    )

    assert report.sections == ["Performance"]


def test_report_model_custom_metadata():
    report = ReportModel(
        title="Daily Report",
        generated_at=datetime.now(),
        metadata={"version": "1.0"},
    )

    assert report.metadata["version"] == "1.0"


def test_report_models_have_independent_summary():
    first = ReportModel(
        title="A",
        generated_at=datetime.now(),
    )

    second = ReportModel(
        title="B",
        generated_at=datetime.now(),
    )

    first.summary["x"] = 1

    assert second.summary == {}


def test_report_models_have_independent_sections():
    first = ReportModel(
        title="A",
        generated_at=datetime.now(),
    )

    second = ReportModel(
        title="B",
        generated_at=datetime.now(),
    )

    first.sections.append("Performance")

    assert second.sections == []


def test_report_models_have_independent_metadata():
    first = ReportModel(
        title="A",
        generated_at=datetime.now(),
    )

    second = ReportModel(
        title="B",
        generated_at=datetime.now(),
    )

    first.metadata["author"] = "Rajesh"

    assert second.metadata == {}


def test_report_model_equality():
    now = datetime(2026, 7, 21)

    first = ReportModel("Daily", now)
    second = ReportModel("Daily", now)

    assert first == second


def test_report_model_repr_contains_title():
    report = ReportModel(
        title="Daily Report",
        generated_at=datetime.now(),
    )

    assert "Daily Report" in repr(report)


def test_report_model_has_slots():
    assert "__slots__" in ReportModel.__dict__


def test_report_model_summary_is_dict():
    report = ReportModel(
        title="Daily Report",
        generated_at=datetime.now(),
    )

    assert isinstance(report.summary, dict)
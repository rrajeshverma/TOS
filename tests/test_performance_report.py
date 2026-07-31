from reporting.models.performance_model import PerformanceModel
from reporting.reports.performance_report import PerformanceReport


def build_report():
    performance = PerformanceModel()
    return PerformanceReport(performance=performance)


# ============================================================
# Constructor
# ============================================================


def test_create_performance_report():
    performance = PerformanceModel()

    report = PerformanceReport(
        performance=performance,
    )

    assert report is not None
    assert report.performance is performance


# ============================================================
# Summary
# ============================================================


def test_default_summary_is_empty():
    report = build_report()

    assert report.summary == ""


def test_custom_summary():
    performance = PerformanceModel()

    report = PerformanceReport(
        performance=performance,
        summary="Trading Summary",
    )

    assert report.summary == "Trading Summary"


# ============================================================
# Helper Methods
# ============================================================


def test_has_summary_false():
    report = build_report()

    assert report.has_summary() is False


def test_has_summary_true():
    performance = PerformanceModel()

    report = PerformanceReport(
        performance=performance,
        summary="Completed",
    )

    assert report.has_summary() is True


def test_update_summary():
    report = build_report()

    report.update_summary("Daily Report")

    assert report.summary == "Daily Report"


def test_clear_summary():
    performance = PerformanceModel()

    report = PerformanceReport(
        performance=performance,
        summary="Hello",
    )

    report.clear_summary()

    assert report.summary == ""


# ============================================================
# Dictionary
# ============================================================


def test_to_dict_returns_dictionary():
    report = build_report()

    assert isinstance(report.to_dict(), dict)


def test_to_dict_contains_performance():
    report = build_report()

    assert "performance" in report.to_dict()


def test_to_dict_contains_summary():
    report = build_report()

    assert "summary" in report.to_dict()


# ============================================================
# Report Name
# ============================================================


def test_report_name():
    report = build_report()

    assert report.report_name() == "Performance Report"


# ============================================================
# Repeatability
# ============================================================


def test_to_dict_repeatable():
    report = build_report()

    assert report.to_dict() == report.to_dict()


def test_to_dict_returns_new_object():
    report = build_report()

    assert report.to_dict() is not report.to_dict()


def test_summary_after_update():
    report = build_report()

    report.update_summary("ABC")

    assert report.to_dict()["summary"] == "ABC"


def test_summary_after_clear():
    report = build_report()

    report.update_summary("ABC")
    report.clear_summary()

    assert report.summary == ""

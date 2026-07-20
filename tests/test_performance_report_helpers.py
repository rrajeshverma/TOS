from reporting.models.performance_model import PerformanceModel
from reporting.reports.performance_report import PerformanceReport


def build_report(summary=""):
    return PerformanceReport(
        performance=PerformanceModel(),
        summary=summary,
    )


def test_is_empty_true():
    report = build_report()
    assert report.is_empty() is True


def test_is_empty_false():
    report = build_report("Daily Report")
    assert report.is_empty() is False


def test_summary_length_zero():
    report = build_report()
    assert report.summary_length() == 0


def test_summary_length():
    report = build_report("ABC")
    assert report.summary_length() == 3


def test_append_summary():
    report = build_report("ABC")

    report.append_summary(" DEF")

    assert report.summary == "ABC DEF"


def test_append_summary_empty():
    report = build_report()

    report.append_summary("Hello")

    assert report.summary == "Hello"


def test_copy():
    report = build_report("Test")

    copied = report.copy()

    assert copied is not report


def test_copy_summary():
    report = build_report("Test")

    copied = report.copy()

    assert copied.summary == "Test"


def test_copy_performance():
    report = build_report()

    copied = report.copy()

    assert copied.performance is report.performance


def test_copy_type():
    report = build_report()

    copied = report.copy()

    assert isinstance(copied, PerformanceReport)


def test_append_twice():
    report = build_report("A")

    report.append_summary("B")
    report.append_summary("C")

    assert report.summary == "ABC"


def test_summary_length_after_append():
    report = build_report("ABC")

    report.append_summary("DEF")

    assert report.summary_length() == 6


def test_copy_independent_summary():
    report = build_report("ABC")

    copied = report.copy()
    copied.update_summary("XYZ")

    assert report.summary == "ABC"
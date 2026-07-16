from reporting.models.performance_model import PerformanceModel
from reporting.reports.performance_report import PerformanceReport


def test_create_performance_report():
    performance = PerformanceModel()

    report = PerformanceReport(
        performance=performance,
    )

    assert report is not None
    assert report.performance is performance
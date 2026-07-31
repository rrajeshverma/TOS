from reporting.report_builder import ReportBuilder
from reporting.report_model import ReportModel


def test_builder_creation():
    builder = ReportBuilder()
    assert builder is not None


def test_build_returns_report_model():
    builder = ReportBuilder()

    report = builder.build("Daily", [])

    assert isinstance(report, ReportModel)


def test_build_preserves_title():
    builder = ReportBuilder()

    report = builder.build("Daily Report", [])

    assert report.title == "Daily Report"


def test_generated_at_exists():
    builder = ReportBuilder()

    report = builder.build("Daily", [])

    assert report.generated_at is not None


def test_empty_trade_count():
    builder = ReportBuilder()

    report = builder.build("Daily", [])

    assert report.summary["total_trades"] == 0


def test_trade_count():
    builder = ReportBuilder()

    report = builder.build("Daily", [100, -50, 25])

    assert report.summary["total_trades"] == 3


def test_total_profit():
    builder = ReportBuilder()

    report = builder.build("Daily", [100, -50, 25])

    assert report.summary["total_profit"] == 75


def test_win_count():
    builder = ReportBuilder()

    report = builder.build("Daily", [100, -50, 25])

    assert report.summary["win_count"] == 2


def test_loss_count():
    builder = ReportBuilder()

    report = builder.build("Daily", [100, -50, 25])

    assert report.summary["loss_count"] == 1


def test_win_rate():
    builder = ReportBuilder()

    report = builder.build("Daily", [100, -50, 25, -10])

    assert report.summary["win_rate"] == 50.0


def test_summary_exists():
    builder = ReportBuilder()

    report = builder.build("Daily", [])

    assert isinstance(report.summary, dict)


def test_builder_repeatable():
    builder = ReportBuilder()

    r1 = builder.build("One", [])
    r2 = builder.build("Two", [])

    assert r1.title != r2.title


def test_independent_reports():
    builder = ReportBuilder()

    r1 = builder.build("One", [])
    r2 = builder.build("Two", [])

    assert r1 is not r2


def test_empty_summary_keys():
    builder = ReportBuilder()

    report = builder.build("Daily", [])

    assert "total_profit" in report.summary


def test_builder_class_exists():
    assert ReportBuilder is not None

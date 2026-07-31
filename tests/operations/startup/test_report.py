from operations.startup.report import (
    ValidationIssue,
    ValidationReport,
    ValidationStatus,
)


def test_validation_issue_defaults():
    issue = ValidationIssue("Config")

    assert issue.name == "Config"
    assert issue.status == ValidationStatus.PASS
    assert issue.message == ""


def test_validation_issue_with_message():
    issue = ValidationIssue(
        name="Broker",
        status=ValidationStatus.FAIL,
        message="API Key Missing",
    )

    assert issue.message == "API Key Missing"


def test_validation_report_empty():
    report = ValidationReport()

    assert len(report.issues) == 0


def test_add_issue():
    report = ValidationReport()

    report.add(ValidationIssue("Config"))

    assert len(report.issues) == 1


def test_multiple_issues():
    report = ValidationReport()

    report.add(ValidationIssue("Config"))
    report.add(ValidationIssue("Broker"))

    assert len(report.issues) == 2


def test_pass_count():
    report = ValidationReport()

    report.add(ValidationIssue("A"))
    report.add(ValidationIssue("B"))

    assert report.pass_count == 2


def test_fail_count():
    report = ValidationReport()

    report.add(
        ValidationIssue(
            "Broker",
            ValidationStatus.FAIL,
        )
    )

    assert report.fail_count == 1


def test_warning_count():
    report = ValidationReport()

    report.add(
        ValidationIssue(
            "Disk",
            ValidationStatus.WARNING,
        )
    )

    assert report.warning_count == 1


def test_is_success_true():
    report = ValidationReport()

    report.add(ValidationIssue("Config"))

    assert report.success


def test_is_success_false():
    report = ValidationReport()

    report.add(
        ValidationIssue(
            "Broker",
            ValidationStatus.FAIL,
        )
    )

    assert not report.success


def test_health_score_all_pass():
    report = ValidationReport()

    for i in range(5):
        report.add(ValidationIssue(str(i)))

    assert report.health_score == 100


def test_health_score_half():
    report = ValidationReport()

    report.add(ValidationIssue("A"))

    report.add(
        ValidationIssue(
            "B",
            ValidationStatus.FAIL,
        )
    )

    assert report.health_score == 50


def test_health_score_zero():
    report = ValidationReport()

    report.add(
        ValidationIssue(
            "A",
            ValidationStatus.FAIL,
        )
    )

    assert report.health_score == 0


def test_report_iterable():
    report = ValidationReport()

    report.add(ValidationIssue("A"))

    assert len(list(report)) == 1


def test_report_len():
    report = ValidationReport()

    report.add(ValidationIssue("A"))

    assert len(report) == 1


def test_report_repr():
    report = ValidationReport()

    assert "ValidationReport" in repr(report)


def test_issue_repr():
    issue = ValidationIssue("Config")

    assert "Config" in repr(issue)


def test_issue_status_enum():
    assert ValidationStatus.PASS.value == "PASS"


def test_warning_enum():
    assert ValidationStatus.WARNING.value == "WARNING"


def test_fail_enum():
    assert ValidationStatus.FAIL.value == "FAIL"

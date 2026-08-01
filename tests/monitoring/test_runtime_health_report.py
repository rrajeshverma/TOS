from monitoring.runtime_health_report import RuntimeHealthReport


def test_report_stores_broker():
    assert (
        RuntimeHealthReport(
            "CONNECTED",
            "AVAILABLE",
        ).broker
        == "CONNECTED"
    )


def test_report_stores_reconnect():
    assert (
        RuntimeHealthReport(
            "CONNECTED",
            "AVAILABLE",
        ).reconnect
        == "AVAILABLE"
    )


def test_connected_blocked_is_healthy():
    report = RuntimeHealthReport(
        "CONNECTED",
        "BLOCKED",
    )

    assert report.healthy


def test_disconnected_not_healthy():
    assert (
        RuntimeHealthReport(
            "DISCONNECTED",
            "AVAILABLE",
        ).healthy
        is False
    )


def test_disconnected_available_is_not_healthy():
    report = RuntimeHealthReport(
        "DISCONNECTED",
        "AVAILABLE",
    )

    assert report.healthy is False


def test_report_is_frozen():
    assert RuntimeHealthReport.__dataclass_params__.frozen


def test_report_has_slots():
    assert hasattr(
        RuntimeHealthReport(
            "CONNECTED",
            "AVAILABLE",
        ),
        "__slots__",
    )


def test_reports_compare_equal():
    assert RuntimeHealthReport(
        "CONNECTED",
        "AVAILABLE",
    ) == RuntimeHealthReport(
        "CONNECTED",
        "AVAILABLE",
    )


def test_reports_can_compare_not_equal():
    assert RuntimeHealthReport(
        "CONNECTED",
        "AVAILABLE",
    ) != RuntimeHealthReport(
        "DISCONNECTED",
        "BLOCKED",
    )


def test_healthy_returns_boolean():
    assert isinstance(
        RuntimeHealthReport(
            "CONNECTED",
            "AVAILABLE",
        ).healthy,
        bool,
    )

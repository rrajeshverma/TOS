from trading.live_audit import (
    LiveAuditLogger,
)


def test_live_enable_creates_audit_record():
    audit = LiveAuditLogger()

    record = audit.record_enable(
        operator="RAJESH",
        reason="Production validation",
    )

    assert record.operator == "RAJESH"

    assert record.reason == "Production validation"


def test_audit_count_increases():
    audit = LiveAuditLogger()

    audit.record_enable(
        operator="SYSTEM",
        reason="Manual approval",
    )

    assert audit.count() == 1


def test_multiple_live_enable_events_are_saved():
    audit = LiveAuditLogger()

    audit.record_enable(
        "USER1",
        "Test",
    )

    audit.record_enable(
        "USER2",
        "Release",
    )

    assert audit.count() == 2


def test_audit_records_are_read_only_copy():
    audit = LiveAuditLogger()

    audit.record_enable(
        "USER",
        "Reason",
    )

    records = audit.records

    records.clear()

    assert audit.count() == 1


def test_timestamp_exists():
    audit = LiveAuditLogger()

    record = audit.record_enable(
        "USER",
        "Enable live",
    )

    assert record.timestamp is not None

"""
Integration Test:

Execution Mode + Live Audit Integration

Validates:
- LIVE mode requires approval
- Approval creates audit record
- Execution becomes enabled after approval
- Multiple approvals are tracked
"""

from trading.execution_mode import (
    ExecutionMode,
    ExecutionModeGuard,
)

from trading.live_audit import (
    LiveAuditLogger,
)


def enable_live_with_audit(
    guard,
    audit,
    operator,
    reason,
):

    record = audit.record_enable(
        operator,
        reason,
    )

    guard.enable_live_trading()

    return record



def test_live_mode_disabled_before_approval():

    guard = ExecutionModeGuard(
        ExecutionMode.LIVE
    )

    assert (
        guard.can_execute()
        is False
    )



def test_live_enable_creates_audit_and_unlocks():

    guard = ExecutionModeGuard(
        ExecutionMode.LIVE
    )

    audit = LiveAuditLogger()


    record = enable_live_with_audit(
        guard,
        audit,
        "RAJESH",
        "Production validation",
    )


    assert (
        record.operator
        == "RAJESH"
    )

    assert (
        audit.count()
        == 1
    )

    assert (
        guard.can_execute()
        is True
    )



def test_live_audit_reason_is_preserved():

    guard = ExecutionModeGuard(
        ExecutionMode.LIVE
    )

    audit = LiveAuditLogger()


    enable_live_with_audit(
        guard,
        audit,
        "ADMIN",
        "Morning trading session",
    )


    record = audit.records[0]


    assert (
        record.reason
        == "Morning trading session"
    )



def test_multiple_live_sessions_are_audited():

    guard = ExecutionModeGuard(
        ExecutionMode.LIVE
    )

    audit = LiveAuditLogger()


    enable_live_with_audit(
        guard,
        audit,
        "USER1",
        "Session 1",
    )

    enable_live_with_audit(
        guard,
        audit,
        "USER2",
        "Session 2",
    )


    assert (
        audit.count()
        == 2
    )



def test_emergency_disable_after_live_enable():

    guard = ExecutionModeGuard(
        ExecutionMode.LIVE
    )

    audit = LiveAuditLogger()


    enable_live_with_audit(
        guard,
        audit,
        "RAJESH",
        "Live execution",
    )


    assert (
        guard.can_execute()
        is True
    )


    guard.disable_live_trading()


    assert (
        guard.can_execute()
        is False
    )

"""
Tests for RuntimeHealth.
"""

from runtime.runtime_health import RuntimeHealth
from runtime.session_state import SessionState
from shared.runtime_status import RuntimeStatus


def test_runtime_health():
    health = RuntimeHealth(
        runtime_status=RuntimeStatus.RUNNING,
        session_state=SessionState.OPEN,
        broker_connected=True,
        market_data_connected=True,
        trading_allowed=True,
    )

    assert health.runtime_status == RuntimeStatus.RUNNING
    assert health.session_state == SessionState.OPEN
    assert health.broker_connected
    assert health.market_data_connected
    assert health.trading_allowed

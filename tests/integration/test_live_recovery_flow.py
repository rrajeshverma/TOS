"""
Integration test:
Runtime Failure -> Recovery -> Resume Trading
"""

from monitoring.runtime_status import RuntimeStatus
from market.websocket_feed import WebSocketFeed
from services.exit_manager import ExitManager


def test_runtime_can_recover_after_stop():

    status = RuntimeStatus()

    status.start()

    assert status.is_running is True

    status.stop()

    assert status.is_running is False

    status.start()

    assert status.is_running is True


def test_market_feed_reconnect_flow():

    feed = WebSocketFeed()

    assert feed.is_connected() is False

    feed.connect()

    assert feed.is_connected() is True

    feed.disconnect()

    assert feed.is_connected() is False

    feed.connect()

    assert feed.is_connected() is True


def test_recovery_keeps_runtime_safe_state():

    status = RuntimeStatus()

    status.start()

    feed = WebSocketFeed()

    feed.connect()

    health = {
        "runtime": status.is_running,
        "market_feed": feed.is_connected(),
    }

    assert health["runtime"] is True
    assert health["market_feed"] is True


def test_exit_manager_available_for_failure_exit():

    manager = ExitManager()

    assert manager is not None

def test_order_failure_does_not_crash_runtime():

    from execution.execution_engine import ExecutionEngine
    from execution.execution_request import ExecutionRequest


    class FailedOrderService:

        def submit(self, request):
            raise RuntimeError(
                "Broker unavailable"
            )


    engine = ExecutionEngine(
        FailedOrderService()
    )

    result = engine.execute(
        ExecutionRequest(
            symbol="NIFTY",
            side="BUY",
            quantity=65,
        )
    )

    assert result.success is False
    assert "Broker unavailable" in result.error


def test_market_feed_can_resume_after_failure():

    feed = WebSocketFeed()

    feed.connect()

    assert feed.is_connected() is True

    feed.disconnect()

    assert feed.is_connected() is False

    feed.connect()

    assert feed.is_connected() is True


def test_runtime_health_after_recovery():

    status = RuntimeStatus()

    status.start()

    status.stop()

    status.start()

    assert status.is_running is True
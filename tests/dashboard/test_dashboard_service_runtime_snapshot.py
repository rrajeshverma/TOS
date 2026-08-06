from dashboard.dashboard_service import DashboardService
from runtime.runtime_mode import RuntimeMode
from runtime.trading_runtime import TradingRuntime


def test_get_runtime_snapshot():
    runtime = TradingRuntime(
        services={},
        mode=RuntimeMode.PAPER,
    )

    service = DashboardService()

    snapshot = service.get_runtime_snapshot(runtime)

    assert snapshot.status == "INITIALIZING"
    assert snapshot.mode == "PAPER"
    assert snapshot.running is False
    assert snapshot.metrics["orders_submitted"] == 0

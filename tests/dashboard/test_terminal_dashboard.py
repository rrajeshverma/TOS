from dashboard.terminal_dashboard import TerminalDashboard
from runtime.runtime_mode import RuntimeMode
from runtime.trading_runtime import TradingRuntime


def create_runtime():
    return TradingRuntime(
        services={},
        mode=RuntimeMode.PAPER,
    )


def test_dashboard_initial_state():
    dashboard = TerminalDashboard()

    assert dashboard.running is False
    assert dashboard.started_at is None


def test_dashboard_start():
    dashboard = TerminalDashboard()

    dashboard.start()

    assert dashboard.running is True
    assert dashboard.started_at is not None


def test_dashboard_stop():
    dashboard = TerminalDashboard()

    dashboard.start()
    dashboard.stop()

    assert dashboard.running is False


def test_dashboard_render():
    dashboard = TerminalDashboard()
    runtime = create_runtime()

    output = dashboard.render(runtime)

    assert "Trading Operating System Dashboard" in output


def test_dashboard_refresh():
    dashboard = TerminalDashboard()

    dashboard.refresh()

    assert dashboard.running is False


def test_dashboard_contains_all_widgets():
    dashboard = TerminalDashboard()
    runtime = create_runtime()

    output = dashboard.render(runtime)

    assert "Runtime" in output
    assert "Broker" in output
    assert "Market" in output
    assert "Portfolio" in output
    assert "Risk" in output
    assert "System" in output
    assert "Alerts" in output


def test_dashboard_start_stop():
    dashboard = TerminalDashboard()

    dashboard.start()

    assert dashboard.running is True

    dashboard.stop()

    assert dashboard.running is False

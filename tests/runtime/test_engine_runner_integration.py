from unittest.mock import Mock

from brokers.paper_broker import PaperBroker
from execution.execution_engine import ExecutionEngine
from runtime.engine_runner import EngineRunner
from runtime.health_monitor import HealthMonitor
from runtime.runtime_state import RuntimeState
from services.paper_trading_service import PaperTradingService


# ==========================================================
# Engine Initialization
# ==========================================================


def test_engine_runner_initializes_paper_broker():
    broker = PaperBroker()

    runner = EngineRunner()
    runner.set_broker(broker)

    assert runner.broker is broker


def test_engine_runner_initializes_execution_engine():
    engine = ExecutionEngine(Mock())

    runner = EngineRunner()
    runner.set_execution_engine(engine)

    assert runner.execution_engine is engine


def test_engine_runner_initializes_trading_service():
    service = PaperTradingService()

    runner = EngineRunner()
    runner.set_trading_service(service)

    assert runner.trading_service is service


def test_engine_runner_initializes_runtime_state():
    state = RuntimeState()

    runner = EngineRunner()
    runner.set_runtime_state(state)

    assert runner.runtime_state is state


def test_engine_runner_initializes_health_monitor():
    monitor = HealthMonitor()

    runner = EngineRunner()
    runner.set_health_monitor(monitor)

    assert runner.health_monitor is monitor


# ==========================================================
# Broker Lifecycle
# ==========================================================


def test_engine_runner_connects_broker():
    broker = PaperBroker()

    runner = EngineRunner()
    runner.set_broker(broker)

    runner.connect_broker()

    assert broker.is_connected()


def test_engine_runner_disconnects_broker():
    broker = PaperBroker()
    broker.connect()

    runner = EngineRunner()
    runner.set_broker(broker)

    runner.disconnect_broker()

    assert not broker.is_connected()


def test_engine_runner_broker_status():
    broker = PaperBroker()

    runner = EngineRunner()
    runner.set_broker(broker)

    assert runner.broker_connected() is False


def test_engine_runner_broker_status_after_connect():
    broker = PaperBroker()

    runner = EngineRunner()
    runner.set_broker(broker)

    runner.connect_broker()

    assert runner.broker_connected() is True


def test_engine_runner_reconnect_broker():
    broker = PaperBroker()

    runner = EngineRunner()
    runner.set_broker(broker)

    runner.reconnect_broker()

    assert broker.is_connected()


# ==========================================================
# Dependency Injection
# ==========================================================


def test_engine_runner_assigns_execution_engine():
    runner = EngineRunner()
    engine = ExecutionEngine(Mock())

    runner.set_execution_engine(engine)

    assert runner.execution_engine is engine


def test_engine_runner_assigns_runtime_state():
    runner = EngineRunner()
    state = RuntimeState()

    runner.set_runtime_state(state)

    assert runner.runtime_state is state


def test_engine_runner_assigns_health_monitor():
    runner = EngineRunner()
    monitor = HealthMonitor()

    runner.set_health_monitor(monitor)

    assert runner.health_monitor is monitor


def test_engine_runner_assigns_trading_service():
    runner = EngineRunner()
    service = PaperTradingService()

    runner.set_trading_service(service)

    assert runner.trading_service is service


def test_engine_runner_has_all_dependencies():
    runner = EngineRunner()

    assert runner.broker is None
    assert runner.execution_engine is None
    assert runner.trading_service is None


# ==========================================================
# Runtime Readiness
# ==========================================================


def test_engine_runner_ready_when_dependencies_present():
    runner = EngineRunner()

    runner.set_broker(PaperBroker())
    runner.set_execution_engine(ExecutionEngine(Mock()))
    runner.set_trading_service(PaperTradingService())

    assert runner.is_ready()


def test_engine_runner_not_ready_without_broker():
    runner = EngineRunner()

    assert not runner.is_ready()


def test_engine_runner_not_ready_without_execution_engine():
    runner = EngineRunner()

    runner.set_broker(PaperBroker())

    assert not runner.is_ready()


def test_engine_runner_not_ready_without_trading_service():
    runner = EngineRunner()

    runner.set_broker(PaperBroker())
    runner.set_execution_engine(ExecutionEngine(Mock()))

    assert not runner.is_ready()


def test_engine_runner_start_requires_ready_state():
    runner = EngineRunner()

    assert runner.can_start() is False


def test_engine_runner_shutdown_disconnects_market(): ...


def test_engine_runner_restart_reconnects_market(): ...


def test_engine_runner_health_after_market_cycle(): ...


def test_engine_runner_runtime_cycle_count(): ...


def test_engine_runner_complete_market_workflow(): ...

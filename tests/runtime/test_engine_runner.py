from unittest.mock import MagicMock, Mock

from runtime.engine_runner import EngineRunner


def test_engine_runner_initial_state():
    runner = EngineRunner()

    assert runner.running is False
    assert runner.cycles == 0
    assert runner.broker is None
    assert runner.execution_engine is None
    assert runner.trading_service is None
    assert runner.runtime_state is None
    assert runner.health_monitor is None


def test_set_broker():
    runner = EngineRunner()
    broker = Mock()

    runner.set_broker(broker)

    assert runner.broker is broker


def test_set_execution_engine():
    runner = EngineRunner()
    execution_engine = Mock()

    runner.set_execution_engine(execution_engine)

    assert runner.execution_engine is execution_engine


def test_set_trading_service():
    runner = EngineRunner()
    trading_service = Mock()

    runner.set_trading_service(trading_service)

    assert runner.trading_service is trading_service


def test_set_runtime_state():
    runner = EngineRunner()
    runtime_state = Mock()

    runner.set_runtime_state(runtime_state)

    assert runner.runtime_state is runtime_state


def test_set_health_monitor():
    runner = EngineRunner()
    health_monitor = Mock()

    runner.set_health_monitor(health_monitor)

    assert runner.health_monitor is health_monitor


def test_connect_broker():
    runner = EngineRunner()
    broker = Mock()

    runner.set_broker(broker)

    runner.connect_broker()

    broker.connect.assert_called_once()


def test_disconnect_broker():
    runner = EngineRunner()
    broker = Mock()

    runner.set_broker(broker)

    runner.disconnect_broker()

    broker.disconnect.assert_called_once()


def test_reconnect_broker():
    runner = EngineRunner()
    broker = Mock()

    runner.set_broker(broker)

    runner.reconnect_broker()

    broker.disconnect.assert_called_once()
    broker.connect.assert_called_once()


def test_broker_connected_true():
    runner = EngineRunner()
    broker = Mock()

    broker.is_connected.return_value = True

    runner.set_broker(broker)

    assert runner.broker_connected() is True


def test_broker_connected_false_without_broker():
    runner = EngineRunner()

    assert runner.broker_connected() is False


def test_is_ready_false_initially():
    runner = EngineRunner()

    assert runner.is_ready() is False


def test_is_ready_true():
    runner = EngineRunner()

    runner.set_broker(Mock())
    runner.set_execution_engine(Mock())
    runner.set_trading_service(Mock())

    assert runner.is_ready() is True


def test_can_start():
    runner = EngineRunner()

    runner.set_broker(Mock())
    runner.set_execution_engine(Mock())
    runner.set_trading_service(Mock())

    assert runner.can_start() is True


def test_engine_runner_start():
    runner = EngineRunner()

    runner.start()

    assert runner.running is True


def test_engine_runner_stop():
    runner = EngineRunner()

    runner.start()
    runner.stop()

    assert runner.running is False


def test_engine_runner_restart():
    runner = EngineRunner()

    runner.restart()

    assert runner.running is True


def test_engine_runner_runs_cycle():
    runner = EngineRunner()

    runner.run_cycle()

    assert runner.cycles == 1


def test_engine_runner_handles_multiple_cycles():
    runner = EngineRunner()

    runner.run_cycle()
    runner.run_cycle()
    runner.run_cycle()

    assert runner.cycles == 3


def test_engine_runner_is_running():
    runner = EngineRunner()

    runner.start()

    assert runner.is_running() is True


def test_engine_runner_shutdown():
    runner = EngineRunner()
    broker = Mock()

    runner.set_broker(broker)
    runner.start()

    runner.shutdown()

    assert runner.running is False
    broker.disconnect.assert_called_once()

def test_restart_stops_and_starts():
    runner = EngineRunner()

    runner.start()
    assert runner.is_running()

    runner.restart()

    assert runner.is_running()


def test_shutdown_disconnects_broker():
    broker = MagicMock()

    runner = EngineRunner()
    runner.set_broker(broker)

    runner.start()
    runner.shutdown()

    broker.disconnect.assert_called_once_with()
    assert not runner.is_running()


def test_shutdown_without_broker():
    runner = EngineRunner()

    runner.shutdown()

    assert not runner.is_running()


def test_cycles_increment():
    runner = EngineRunner()

    assert runner.cycles == 0

    runner.run_cycle()
    runner.run_cycle()

    assert runner.cycles == 2
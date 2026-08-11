from unittest.mock import Mock

from runtime.runtime_mode import RuntimeMode
from runtime.session_state import SessionState
from runtime.trading_runtime import TradingRuntime
from shared.events import Event
from shared.runtime_status import RuntimeStatus


def test_start_registers_market_data_callback():
    market_data = Mock()
    trading_pipeline = Mock()

    runtime = TradingRuntime(
        {
            "market_data_service": market_data,
            "trading_pipeline": trading_pipeline,
        }
    )

    runtime.start()

    market_data.register_tick_callback.assert_called_once_with(trading_pipeline.on_tick)


def test_start_connects_market_data():
    market_data = Mock()

    runtime = TradingRuntime(
        {
            "market_data_service": market_data,
        }
    )

    runtime.start()

    market_data.connect.assert_called_once_with()


def test_stop_disconnects_market_data():
    market_data = Mock()

    runtime = TradingRuntime(
        {
            "market_data_service": market_data,
        }
    )

    runtime.stop()

    market_data.disconnect.assert_called_once_with()


def test_run_cycle_uses_indicator_engine():
    indicator_engine = Mock()
    indicator_engine.calculate.return_value = "INDICATORS"

    strategy_engine = Mock()
    strategy_engine.evaluate.return_value = "DECISION"

    risk_engine = Mock()
    risk_engine.evaluate.return_value = "RISK"

    runtime = TradingRuntime(
        {
            "indicator_engine": indicator_engine,
            "strategy_engine": strategy_engine,
            "risk_engine": risk_engine,
        }
    )

    market = Mock()
    history = [market]

    runtime.run_cycle(
        market,
        history,
    )

    indicator_engine.calculate.assert_called_once_with(history)


def test_run_cycle_uses_strategy_decide():
    indicator_engine = Mock()
    indicator_engine.calculate.return_value = "INDICATORS"

    strategy_engine = Mock()
    strategy_engine.decide.return_value = "DECISION"

    risk_engine = Mock()
    risk_engine.evaluate.return_value = "RISK"

    runtime = TradingRuntime(
        {
            "indicator_engine": indicator_engine,
            "strategy_engine": strategy_engine,
            "risk_engine": risk_engine,
        }
    )

    market = Mock()
    history = [market]

    runtime.run_cycle(market, history)

    strategy_engine.decide.assert_called_once_with(
        market,
        "INDICATORS",
    )


def test_run_cycle_uses_risk_engine():
    indicator_engine = Mock()
    indicator_engine.calculate.return_value = "INDICATORS"

    strategy_engine = Mock()
    strategy_engine.decide.return_value = "DECISION"

    risk_engine = Mock()
    risk_engine.evaluate.return_value = "RISK"

    runtime = TradingRuntime(
        {
            "indicator_engine": indicator_engine,
            "strategy_engine": strategy_engine,
            "risk_engine": risk_engine,
        }
    )

    market = Mock()
    history = [market]

    result = runtime.run_cycle(
        market,
        history,
    )

    risk_engine.evaluate.assert_called_once_with(
        "DECISION",
        trades_today=0,
        daily_loss=0,
    )

    assert result == "RISK"


def test_run_cycle_uses_execution_manager():
    indicator_engine = Mock()
    indicator_engine.calculate.return_value = "INDICATORS"

    strategy_engine = Mock()
    strategy_engine.decide.return_value = "DECISION"

    risk = Mock()
    risk_engine = Mock()
    risk_engine.evaluate.return_value = risk

    execution_result = Mock()

    execution_manager = Mock()
    execution_manager.execute.return_value = execution_result

    runtime = TradingRuntime(
        {
            "indicator_engine": indicator_engine,
            "strategy_engine": strategy_engine,
            "risk_engine": risk_engine,
            "execution_manager": execution_manager,
        }
    )

    market = Mock()
    history = [market]

    result = runtime.run_cycle(
        market,
        history,
    )

    execution_manager.execute.assert_called_once_with(risk)
    assert result is execution_result


def test_constructor_exposes_runtime_services():
    indicator_engine = Mock()
    strategy_engine = Mock()
    risk_engine = Mock()
    execution_manager = Mock()

    runtime = TradingRuntime(
        {
            "indicator_engine": indicator_engine,
            "strategy_engine": strategy_engine,
            "risk_engine": risk_engine,
            "execution_manager": execution_manager,
        }
    )

    assert runtime.indicator_engine is indicator_engine
    assert runtime.strategy_engine is strategy_engine
    assert runtime.risk_engine is risk_engine
    assert runtime.execution_manager is execution_manager


def test_health_reports_runtime_status():
    runtime = TradingRuntime(
        {
            "indicator_engine": Mock(),
            "strategy_engine": Mock(),
            "risk_engine": Mock(),
            "execution_manager": Mock(),
            "market_data_service": Mock(),
            "trading_pipeline": Mock(),
        }
    )

    runtime.running = True

    health = runtime.health()

    assert health["running"] is True
    assert health["services"] == [
        "indicator_engine",
        "strategy_engine",
        "risk_engine",
        "execution_manager",
        "market_data_service",
        "trading_pipeline",
    ]


def test_on_market_tick_ignored_when_market_closed():
    runtime = TradingRuntime({})

    runtime.market_clock.current_session = Mock(
        return_value=SessionState.CLOSED,
    )

    runtime.publish = Mock()
    runtime.run_cycle = Mock()

    runtime.on_market_tick(
        Mock(),
        [],
    )

    runtime.publish.assert_not_called()
    runtime.run_cycle.assert_not_called()


def test_runtime_resolves_services_dynamically():
    runtime = TradingRuntime({})

    services = {
        "indicator_engine": Mock(),
        "strategy_engine": Mock(),
        "risk_engine": Mock(),
        "execution_manager": Mock(),
    }

    runtime.services = services

    assert runtime.indicator_engine is services["indicator_engine"]
    assert runtime.strategy_engine is services["strategy_engine"]
    assert runtime.risk_engine is services["risk_engine"]
    assert runtime.execution_manager is services["execution_manager"]


def test_runtime_start_registers_market_tick_handler():
    runtime = TradingRuntime({})

    received = []

    runtime.bus.subscribe(
        Event.MARKET_TICK.value,
        lambda payload: received.append(payload),
    )

    runtime.start()

    runtime.publish(
        Event.MARKET_TICK,
        {
            "market": object(),
            "history": [],
        },
    )

    assert received


def test_validate_reports_missing_services():
    runtime = TradingRuntime({})

    missing = runtime.validate()

    assert sorted(missing) == sorted(
        [
            "indicator_engine",
            "strategy_engine",
            "risk_engine",
            "execution_manager",
            "market_data_service",
            "trading_pipeline",
        ]
    )


def test_validate_returns_empty_when_complete():
    runtime = TradingRuntime(
        {
            "indicator_engine": Mock(),
            "strategy_engine": Mock(),
            "risk_engine": Mock(),
            "execution_manager": Mock(),
            "market_data_service": Mock(),
            "trading_pipeline": Mock(),
        }
    )

    assert runtime.validate() == []


def test_is_running_property():
    runtime = TradingRuntime({})

    assert runtime.is_running is False

    runtime.runtime_status = RuntimeStatus.RUNNING

    assert runtime.is_running is True


def test_pause_changes_runtime_state():
    runtime = TradingRuntime({})

    runtime.pause()

    assert runtime.state == RuntimeStatus.PAUSED


def test_fail_changes_runtime_state():
    runtime = TradingRuntime({})

    runtime.running = True

    runtime.fail()

    assert runtime.running is False
    assert runtime.state == RuntimeStatus.FAILED


def test_backtest_mode_returns_risk_without_execution():
    indicator_engine = Mock()
    indicator_engine.calculate.return_value = "IND"

    strategy_engine = Mock()
    strategy_engine.decide.return_value = "DEC"

    risk = Mock()

    risk_engine = Mock()
    risk_engine.evaluate.return_value = risk

    execution_manager = Mock()

    runtime = TradingRuntime(
        {
            "indicator_engine": indicator_engine,
            "strategy_engine": strategy_engine,
            "risk_engine": risk_engine,
            "execution_manager": execution_manager,
        },
        mode=RuntimeMode.BACKTEST,
    )

    result = runtime.run_cycle(
        Mock(),
        [],
    )

    execution_manager.execute.assert_not_called()

    assert result is risk


def test_handle_market_tick_calls_run_cycle():
    runtime = TradingRuntime({})

    runtime.run_cycle = Mock()

    payload = {
        "market": Mock(),
        "history": [],
    }

    runtime._handle_market_tick(payload)

    runtime.run_cycle.assert_called_once_with(
        payload["market"],
        payload["history"],
    )


def test_on_market_tick_publishes_and_runs_cycle():
    runtime = TradingRuntime({})

    runtime.market_clock.current_session = Mock(
        return_value=SessionState.OPEN,
    )

    runtime.publish = Mock()
    runtime.run_cycle = Mock(return_value="RESULT")

    market = Mock()
    history = []

    result = runtime.on_market_tick(
        market,
        history,
    )

    runtime.publish.assert_called_once_with(
        Event.MARKET_TICK,
        {
            "market": market,
            "history": history,
        },
    )

    runtime.run_cycle.assert_called_once_with(
        market,
        history,
    )

    assert result == "RESULT"


def test_status_returns_runtime_information():
    runtime = TradingRuntime({})

    status = runtime.status()

    assert status["status"] == runtime.runtime_status
    assert status["running"] is False
    assert "metrics" in status


def test_runtime_exposes_trading_pipeline():
    trading_pipeline = Mock()

    runtime = TradingRuntime(
        {
            "trading_pipeline": trading_pipeline,
        }
    )

    assert runtime.trading_pipeline is trading_pipeline


def test_run_cycle_uses_trading_pipeline_when_available():
    trading_pipeline = Mock()

    trading_pipeline.run.return_value = (
        "MARKET",
        "INDICATORS",
        "DECISION",
        "QUALITY",
        "RISK",
        "POSITION_SIZE",
        "TRADE_PLAN",
        "TRADE_MANAGEMENT",
    )

    runtime = TradingRuntime(
        {
            "trading_pipeline": trading_pipeline,
        }
    )

    market = Mock()
    history = [market]

    result = runtime.run_cycle(
        market,
        history,
    )

    trading_pipeline.run.assert_called_once_with(history)

    assert result == "RISK"


def test_run_cycle_executes_pipeline_risk_with_quantity():
    trading_pipeline = Mock()

    risk = Mock()

    position_size = Mock()
    position_size.quantity = 65

    trading_pipeline.run.return_value = (
        "MARKET",
        "INDICATORS",
        "DECISION",
        "QUALITY",
        risk,
        position_size,
        "TRADE_PLAN",
        "TRADE_MANAGEMENT",
    )

    execution_manager = Mock()
    execution_manager.execute.return_value = "EXECUTION"

    runtime = TradingRuntime(
        {
            "trading_pipeline": trading_pipeline,
            "execution_manager": execution_manager,
        }
    )

    result = runtime.run_cycle(
        Mock(),
        [Mock()],
    )

    execution_manager.execute.assert_called_once_with(
        risk,
        quantity=65,
    )

    assert result == "EXECUTION"

from unittest.mock import Mock

from shared.events import Event
from runtime.trading_runtime import TradingRuntime
from runtime.session_state import SessionState


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

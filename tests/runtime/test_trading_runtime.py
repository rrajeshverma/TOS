from unittest.mock import Mock

from runtime.trading_runtime import TradingRuntime


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

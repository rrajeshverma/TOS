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

    market_data.register_tick_callback.assert_called_once_with(
        trading_pipeline.on_tick
    )

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
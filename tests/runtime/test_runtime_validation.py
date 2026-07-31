"""
Tests for TradingRuntime validation.
"""

from runtime.trading_runtime import TradingRuntime


def test_validate_reports_missing_services():
    runtime = TradingRuntime({})

    errors = runtime.validate()

    assert "indicator_engine" in errors
    assert "strategy_engine" in errors
    assert "risk_engine" in errors
    assert "execution_manager" in errors
    assert "market_data_service" in errors
    assert "trading_pipeline" in errors


def test_validate_returns_empty_when_all_services_exist():
    services = {
        "indicator_engine": object(),
        "strategy_engine": object(),
        "risk_engine": object(),
        "execution_manager": object(),
        "market_data_service": object(),
        "trading_pipeline": object(),
    }

    runtime = TradingRuntime(services)

    assert runtime.validate() == []

from datetime import datetime

import pytest

from domain.market import Market
from engines.market_engine import MarketEngine
from exceptions import (
    InvalidPriceError,
    InvalidTimestampError,
    InvalidVolumeError,
    MissingFieldError,
)


@pytest.fixture
def engine():
    return MarketEngine()


@pytest.fixture
def valid_market_data():
    return {
        "symbol": "NIFTY",
        "exchange": "NSE",
        "timeframe": "5m",
        "timestamp": datetime.now(),
        "open": 100.0,
        "high": 105.0,
        "low": 99.0,
        "close": 104.0,
        "volume": 1000,
    }


def test_build_valid_market(engine, valid_market_data):
    market = engine.build_market(valid_market_data)

    assert isinstance(market, Market)
    assert market.symbol == "NIFTY"
    assert market.exchange == "NSE"
    assert market.timeframe == "5m"
    assert market.close == 104.0


def test_none_input(engine):
    with pytest.raises(MissingFieldError):
        engine.build_market(None)


def test_missing_field(engine, valid_market_data):
    del valid_market_data["volume"]

    with pytest.raises(MissingFieldError):
        engine.build_market(valid_market_data)


def test_invalid_timestamp(engine, valid_market_data):
    valid_market_data["timestamp"] = "2026-01-01"

    with pytest.raises(InvalidTimestampError):
        engine.build_market(valid_market_data)


def test_invalid_high_low(engine, valid_market_data):
    valid_market_data["high"] = 90

    with pytest.raises(InvalidPriceError):
        engine.build_market(valid_market_data)


def test_invalid_open(engine, valid_market_data):
    valid_market_data["open"] = 110

    with pytest.raises(InvalidPriceError):
        engine.build_market(valid_market_data)


def test_invalid_close(engine, valid_market_data):
    valid_market_data["close"] = 110

    with pytest.raises(InvalidPriceError):
        engine.build_market(valid_market_data)


def test_negative_volume(engine, valid_market_data):
    valid_market_data["volume"] = -1

    with pytest.raises(InvalidVolumeError):
        engine.build_market(valid_market_data)

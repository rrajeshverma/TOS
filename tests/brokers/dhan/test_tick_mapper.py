from datetime import datetime
from decimal import Decimal

from brokers.dhan.tick_mapper import DhanTickMapper
from brokers.instrument_mapper import InstrumentMapper
from domain.instrument import Instrument
from storage.instrument_repository import InstrumentRepository


def create_mapper():
    repository = InstrumentRepository()

    repository.add(
        Instrument(
            symbol="NIFTY",
            security_id="13",
            exchange_segment="IDX_I",
            lot_size=65,
            tick_size=Decimal("0.05"),
        )
    )

    return DhanTickMapper(
        InstrumentMapper(repository),
    )


def test_dhan_ticker_maps_to_broker_tick():
    mapper = create_mapper()

    timestamp = datetime.now()

    data = {
        "type": "Ticker Data",
        "exchange_segment": 0,
        "security_id": 13,
        "LTP": "24367.75",
        "LTT": timestamp,
    }

    tick = mapper.to_broker_tick(data)

    assert tick.symbol == "NIFTY"
    assert tick.ltp == 24367.75
    assert tick.volume == 0
    assert tick.timestamp == timestamp


def test_unknown_security_id_raises_keyerror():
    mapper = create_mapper()

    data = {
        "type": "Ticker Data",
        "exchange_segment": 0,
        "security_id": 999,
        "LTP": "25000.00",
        "LTT": datetime.now(),
    }

    try:
        mapper.to_broker_tick(data)
        assert False
    except KeyError:
        assert True


def test_dhan_string_ltt_maps_to_datetime():
    mapper = create_mapper()

    data = {
        "type": "Ticker Data",
        "exchange_segment": 0,
        "security_id": 13,
        "LTP": "24367.75",
        "LTT": "14:44:23",
    }

    tick = mapper.to_broker_tick(data)

    assert tick.symbol == "NIFTY"
    assert tick.ltp == 24367.75
    assert tick.volume == 0
    assert isinstance(tick.timestamp, datetime)
    assert tick.timestamp.hour == 14
    assert tick.timestamp.minute == 44
    assert tick.timestamp.second == 23

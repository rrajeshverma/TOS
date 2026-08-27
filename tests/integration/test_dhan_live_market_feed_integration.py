from datetime import datetime
from unittest.mock import Mock, patch

from brokers.dhan.live_market_feed import LiveMarketFeed
from brokers.instrument_mapper import InstrumentMapper
from domain.instrument import Instrument
from storage.instrument_repository import InstrumentRepository


def create_feed():
    repository = InstrumentRepository()

    repository.add(
        Instrument(
            symbol="NIFTY",
            security_id="13",
            exchange_segment="IDX_I",
            lot_size=1,
            tick_size=0.05,
        )
    )

    return LiveMarketFeed(
        client_id="CLIENT",
        access_token="TOKEN",
        instrument_mapper=InstrumentMapper(repository),
    )


@patch("brokers.dhan.live_market_feed.MarketFeed")
def test_live_market_feed_consumes_dhan_quote(mock_market_feed):
    feed = create_feed()
    callback = Mock()

    feed.register_tick_callback(callback)
    feed.subscribe([(0, "13", 17)])

    instance = mock_market_feed.return_value

    packet = {
        "type": "Quote Data",
        "exchange_segment": 0,
        "security_id": 13,
        "LTP": "24340.50",
        "LTT": "14:57:05",
        "last_quantity": 250,
    }

    def run_forever():
        feed._handle_sdk_tick(instance, packet)
        feed._running = False

    instance.run_forever.side_effect = run_forever

    feed._running = True
    feed._run()

    callback.assert_called_once()

    tick = callback.call_args.args[0]

    assert tick.symbol == "NIFTY"
    assert tick.ltp == 24340.50
    assert tick.volume == 250
    assert isinstance(tick.timestamp, datetime)
    assert tick.timestamp.hour == 14
    assert tick.timestamp.minute == 57
    assert tick.timestamp.second == 5

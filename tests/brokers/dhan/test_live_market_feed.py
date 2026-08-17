from datetime import datetime
from unittest.mock import Mock, patch

from brokers.dhan.live_market_feed import LiveMarketFeed
from brokers.dhan.models import BrokerTick


def create_feed():
    instrument_mapper = Mock()

    instrument = Mock()
    instrument.symbol = "NIFTY"

    instrument_mapper.get_by_security_id.return_value = instrument

    return LiveMarketFeed(
        client_id="CLIENT",
        access_token="TOKEN",
        instrument_mapper=instrument_mapper,
    )


def test_initial_state():
    feed = create_feed()

    assert feed.is_running is False
    assert feed.instruments == set()


def test_register_tick_callback():
    feed = create_feed()
    callback = Mock()

    feed.register_tick_callback(callback)

    assert feed._callback is callback


def test_subscribe_before_start():
    feed = create_feed()

    feed.subscribe(
        [(0, "13", 15)],
    )

    assert (0, "13", 15) in feed.instruments


def test_unsubscribe_before_start():
    feed = create_feed()

    feed.subscribe(
        [(0, "13", 15)],
    )

    feed.unsubscribe(
        [(0, "13", 15)],
    )

    assert feed.instruments == set()


def test_tick_is_mapped_and_forwarded():
    feed = create_feed()
    callback = Mock()

    feed.register_tick_callback(callback)

    timestamp = datetime.now()

    data = {
        "type": "Ticker Data",
        "exchange_segment": 0,
        "security_id": 13,
        "LTP": "24367.75",
        "LTT": timestamp,
    }

    feed._on_tick(Mock(), data)

    callback.assert_called_once()

    tick = callback.call_args.args[0]

    assert isinstance(tick, BrokerTick)
    assert tick.symbol == "NIFTY"
    assert tick.ltp == 24367.75
    assert tick.volume == 0
    assert tick.timestamp == timestamp


def test_non_ticker_data_is_ignored():
    feed = create_feed()
    callback = Mock()

    feed.register_tick_callback(callback)

    feed._on_tick(
        Mock(),
        {
            "type": "Quote Data",
        },
    )

    callback.assert_not_called()


def test_start_requires_subscription():
    feed = create_feed()

    try:
        feed.start()
        assert False
    except RuntimeError as exc:
        assert "No instruments subscribed" in str(exc)


@patch("brokers.dhan.live_market_feed.threading.Thread")
def test_start_creates_background_thread(mock_thread):
    feed = create_feed()

    feed.subscribe(
        [(0, "13", 15)],
    )

    thread = mock_thread.return_value

    feed.start()

    assert feed.is_running is True

    mock_thread.assert_called_once()
    thread.start.assert_called_once()


@patch("brokers.dhan.live_market_feed.threading.Thread")
def test_start_is_idempotent(mock_thread):
    feed = create_feed()

    feed.subscribe(
        [(0, "13", 15)],
    )

    feed.start()
    feed.start()

    mock_thread.assert_called_once()


def test_stop_without_start():
    feed = create_feed()

    feed.stop()

    assert feed.is_running is False


@patch("brokers.dhan.live_market_feed.MarketFeed")
def test_run_consumes_sdk_data_and_forwards_ticker(mock_market_feed):
    feed = create_feed()
    callback = Mock()

    feed.register_tick_callback(callback)
    feed.subscribe([(0, "13", 15)])

    instance = mock_market_feed.return_value

    packets = iter(
        [
            {
                "type": "Ticker Data",
                "exchange_segment": 0,
                "security_id": 13,
                "LTP": "24330.60",
                "LTT": "12:53:04",
            },
        ]
    )

    def get_data():
        try:
            return next(packets)
        except StopIteration:
            feed._running = False
            return None

    instance.get_data.side_effect = get_data

    feed._running = True
    feed._run()

    mock_market_feed.assert_called_once()
    instance.run_forever.assert_called_once()
    assert callback.call_count == 1

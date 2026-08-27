from datetime import datetime
from unittest.mock import Mock, patch
from zoneinfo import ZoneInfo

from brokers.dhan.historical_data import DhanHistoricalData


def create_response():
    return {
        "status": "success",
        "remarks": "",
        "data": {
            "open": [100.0, 101.0, 102.0],
            "high": [101.0, 102.0, 103.0],
            "low": [99.0, 100.0, 101.0],
            "close": [100.5, 101.5, 102.5],
            "volume": [1000.0, 1100.0, 1200.0],
            "timestamp": [
                1787038200.0,
                1787038500.0,
                1787038800.0,
            ],
        },
    }


@patch("brokers.dhan.historical_data.dhanhq")
def test_load_nifty_5m_maps_dhan_response(mock_dhanhq):
    client = Mock()
    client.intraday_minute_data.return_value = create_response()
    mock_dhanhq.return_value = client

    adapter = DhanHistoricalData(
        client_id="CLIENT",
        access_token="TOKEN",
    )

    markets = adapter.load_nifty_5m(
        from_date="2026-08-18",
        to_date="2026-08-18",
        limit=50,
    )

    assert len(markets) == 3

    first = markets[0]

    assert first.symbol == "NIFTY"
    assert first.exchange == "NSE"
    assert first.timeframe == "5m"
    assert first.open == 100.0
    assert first.high == 101.0
    assert first.low == 99.0
    assert first.close == 100.5
    assert first.volume == 1000

    client.intraday_minute_data.assert_called_once_with(
        security_id="13",
        exchange_segment="IDX_I",
        instrument_type="INDEX",
        from_date="2026-08-18",
        to_date="2026-08-18",
        interval=5,
    )


@patch("brokers.dhan.historical_data.dhanhq")
def test_load_nifty_5m_sorts_by_timestamp(mock_dhanhq):
    client = Mock()
    response = create_response()

    response["data"]["open"] = [102.0, 100.0, 101.0]
    response["data"]["high"] = [103.0, 101.0, 102.0]
    response["data"]["low"] = [101.0, 99.0, 100.0]
    response["data"]["close"] = [102.5, 100.5, 101.5]
    response["data"]["volume"] = [1200.0, 1000.0, 1100.0]
    response["data"]["timestamp"] = [
        1787038800.0,
        1787038200.0,
        1787038500.0,
    ]

    client.intraday_minute_data.return_value = response
    mock_dhanhq.return_value = client

    adapter = DhanHistoricalData(
        client_id="CLIENT",
        access_token="TOKEN",
    )

    markets = adapter.load_nifty_5m(
        from_date="2026-08-18",
        to_date="2026-08-18",
    )

    assert [market.close for market in markets] == [
        100.5,
        101.5,
        102.5,
    ]


@patch("brokers.dhan.historical_data.dhanhq")
def test_load_nifty_5m_limits_history(mock_dhanhq):
    client = Mock()
    response = create_response()

    response["data"]["open"] = [100.0, 101.0, 102.0]
    response["data"]["high"] = [101.0, 102.0, 103.0]
    response["data"]["low"] = [99.0, 100.0, 101.0]
    response["data"]["close"] = [100.5, 101.5, 102.5]
    response["data"]["volume"] = [1000.0, 1100.0, 1200.0]
    response["data"]["timestamp"] = [
        1787038200.0,
        1787038500.0,
        1787038800.0,
    ]

    client.intraday_minute_data.return_value = response
    mock_dhanhq.return_value = client

    adapter = DhanHistoricalData(
        client_id="CLIENT",
        access_token="TOKEN",
    )

    markets = adapter.load_nifty_5m(
        from_date="2026-08-18",
        to_date="2026-08-18",
        limit=2,
    )

    assert len(markets) == 2
    assert [market.close for market in markets] == [
        101.5,
        102.5,
    ]


@patch("brokers.dhan.historical_data.dhanhq")
def test_load_nifty_5m_rejects_missing_fields(mock_dhanhq):
    client = Mock()
    response = create_response()
    del response["data"]["volume"]

    client.intraday_minute_data.return_value = response
    mock_dhanhq.return_value = client

    adapter = DhanHistoricalData(
        client_id="CLIENT",
        access_token="TOKEN",
    )

    try:
        adapter.load_nifty_5m(
            from_date="2026-08-18",
            to_date="2026-08-18",
        )
        assert False
    except RuntimeError as exc:
        assert "missing candle fields" in str(exc)


@patch("brokers.dhan.historical_data.dhanhq")
def test_load_nifty_5m_rejects_mismatched_arrays(mock_dhanhq):
    client = Mock()
    response = create_response()
    response["data"]["close"] = [100.5, 101.5]

    client.intraday_minute_data.return_value = response
    mock_dhanhq.return_value = client

    adapter = DhanHistoricalData(
        client_id="CLIENT",
        access_token="TOKEN",
    )

    try:
        adapter.load_nifty_5m(
            from_date="2026-08-18",
            to_date="2026-08-18",
        )
        assert False
    except RuntimeError as exc:
        assert "mismatched lengths" in str(exc)


IST = ZoneInfo("Asia/Kolkata")


@patch("brokers.dhan.historical_data.dhanhq")
def test_load_nifty_5m_excludes_currently_forming_candle(
    mock_dhanhq,
):
    client = Mock()

    response = {
        "status": "success",
        "remarks": "",
        "data": {
            "open": [100.0, 101.0, 102.0],
            "high": [101.0, 102.0, 103.0],
            "low": [99.0, 100.0, 101.0],
            "close": [100.5, 101.5, 102.5],
            "volume": [1000.0, 1100.0, 1200.0],
            "timestamp": [
                1787038200.0,
                1787038500.0,
                1787038800.0,
            ],
        },
    }

    client.intraday_minute_data.return_value = response
    mock_dhanhq.return_value = client

    adapter = DhanHistoricalData(
        client_id="CLIENT",
        access_token="TOKEN",
    )

    markets = adapter.load_nifty_5m(
        from_date="2026-08-18",
        to_date="2026-08-18",
        limit=50,
        now=datetime(
            2026,
            8,
            18,
            13,
            12,
            tzinfo=IST,
        ),
    )

    # At 13:12, the 13:10-13:15 candle is still forming.
    assert len(markets) == 2
    assert [market.close for market in markets] == [
        100.5,
        101.5,
    ]

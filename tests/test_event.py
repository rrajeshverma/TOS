from events.event import Event


def test_event_creation():
    event = Event(
        name="PRICE_UPDATED",
        payload={"symbol": "BTCUSDT", "price": 65000},
    )

    assert event.name == "PRICE_UPDATED"
    assert event.payload["symbol"] == "BTCUSDT"
    assert event.payload["price"] == 65000
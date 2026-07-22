from market.websocket_feed import WebSocketFeed


def test_websocket_feed_connect():

    feed = WebSocketFeed()

    feed.connect()

    assert feed.is_connected() is True



def test_websocket_feed_disconnect():

    feed = WebSocketFeed()

    feed.connect()
    feed.disconnect()

    assert feed.is_connected() is False



def test_websocket_feed_initial_state():

    feed = WebSocketFeed()

    assert feed.is_connected() is False



def test_websocket_feed_subscribe():

    feed = WebSocketFeed()

    feed.subscribe("NIFTY")

    assert "NIFTY" in feed.subscriptions



def test_websocket_feed_unsubscribe():

    feed = WebSocketFeed()

    feed.subscribe("NIFTY")
    feed.unsubscribe("NIFTY")

    assert "NIFTY" not in feed.subscriptions
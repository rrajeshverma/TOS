from market.tick_dispatcher import TickDispatcher


def test_register_handler():

    dispatcher = TickDispatcher()

    received = []

    dispatcher.register(
        received.append
    )

    dispatcher.dispatch(
        {
            "symbol": "NIFTY",
            "ltp": 25000,
        }
    )

    assert len(received) == 1



def test_duplicate_handler_is_ignored():

    dispatcher = TickDispatcher()

    received = []


    def handler(tick):
        received.append(tick)


    dispatcher.register(handler)
    dispatcher.register(handler)


    dispatcher.dispatch(
        {
            "symbol": "NIFTY",
            "ltp": 25000,
        }
    )


    assert len(received) == 1



def test_failed_handler_does_not_stop_others():

    dispatcher = TickDispatcher()

    received = []


    def bad(tick):
        raise Exception(
            "handler failed"
        )


    def good(tick):
        received.append(tick)


    dispatcher.register(bad)
    dispatcher.register(good)


    dispatcher.dispatch(
        {
            "symbol": "NIFTY",
            "ltp": 25000,
        }
    )


    assert len(received) == 1



def test_dispatch_returns_failure_count():

    dispatcher = TickDispatcher()


    def bad(tick):
        raise Exception(
            "failed"
        )


    dispatcher.register(bad)


    result = dispatcher.dispatch(
        {
            "symbol": "NIFTY",
            "ltp": 25000,
        }
    )


    assert result["failed"] == 1

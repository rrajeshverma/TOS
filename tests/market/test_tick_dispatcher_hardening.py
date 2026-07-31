from market.tick_dispatcher import TickDispatcher


def test_dispatcher_starts_with_no_handlers():
    dispatcher = TickDispatcher()

    result = dispatcher.dispatch({})

    assert result["dispatched"] is True
    assert result["failed"] == 0


def test_register_single_handler():
    dispatcher = TickDispatcher()

    calls = []

    def handler(tick):
        calls.append(tick)

    dispatcher.register(handler)

    tick = {"ltp": 100}

    dispatcher.dispatch(tick)

    assert calls == [tick]


def test_register_duplicate_handler_only_once():
    dispatcher = TickDispatcher()

    calls = []

    def handler(tick):
        calls.append(tick)

    dispatcher.register(handler)
    dispatcher.register(handler)

    dispatcher.dispatch({"ltp": 1})

    assert len(calls) == 1


def test_unregister_existing_handler():
    dispatcher = TickDispatcher()

    calls = []

    def handler(tick):
        calls.append(tick)

    dispatcher.register(handler)
    dispatcher.unregister(handler)

    dispatcher.dispatch({"ltp": 10})

    assert calls == []


def test_unregister_unknown_handler_is_safe():
    dispatcher = TickDispatcher()

    def handler(tick):
        pass

    dispatcher.unregister(handler)

    result = dispatcher.dispatch({})

    assert result["failed"] == 0


def test_multiple_handlers_receive_same_tick():
    dispatcher = TickDispatcher()

    first = []
    second = []

    def handler1(tick):
        first.append(tick)

    def handler2(tick):
        second.append(tick)

    dispatcher.register(handler1)
    dispatcher.register(handler2)

    tick = {"symbol": "NIFTY"}

    dispatcher.dispatch(tick)

    assert first == [tick]
    assert second == [tick]


def test_dispatch_returns_success():
    dispatcher = TickDispatcher()

    result = dispatcher.dispatch({"a": 1})

    assert result == {
        "dispatched": True,
        "failed": 0,
    }


def test_single_handler_failure_counted():
    dispatcher = TickDispatcher()

    def handler(_):
        raise RuntimeError()

    dispatcher.register(handler)

    result = dispatcher.dispatch({})

    assert result["failed"] == 1


def test_one_handler_failure_does_not_stop_dispatch():
    dispatcher = TickDispatcher()

    calls = []

    def bad(_):
        raise RuntimeError()

    def good(tick):
        calls.append(tick)

    dispatcher.register(bad)
    dispatcher.register(good)

    tick = {"price": 100}

    result = dispatcher.dispatch(tick)

    assert calls == [tick]
    assert result["failed"] == 1


def test_multiple_handler_failures_counted():
    dispatcher = TickDispatcher()

    def bad1(_):
        raise RuntimeError()

    def bad2(_):
        raise ValueError()

    dispatcher.register(bad1)
    dispatcher.register(bad2)

    result = dispatcher.dispatch({})

    assert result["failed"] == 2


def test_unregister_one_of_multiple_handlers():
    dispatcher = TickDispatcher()

    first = []
    second = []

    def handler1(tick):
        first.append(tick)

    def handler2(tick):
        second.append(tick)

    dispatcher.register(handler1)
    dispatcher.register(handler2)

    dispatcher.unregister(handler1)

    dispatcher.dispatch({"x": 1})

    assert first == []
    assert second == [{"x": 1}]


def test_dispatch_empty_tick():
    dispatcher = TickDispatcher()

    calls = []

    def handler(tick):
        calls.append(tick)

    dispatcher.register(handler)

    dispatcher.dispatch({})

    assert calls == [{}]


def test_dispatch_none_tick():
    dispatcher = TickDispatcher()

    calls = []

    def handler(tick):
        calls.append(tick)

    dispatcher.register(handler)

    dispatcher.dispatch(None)

    assert calls == [None]


def test_handler_receives_same_object():
    dispatcher = TickDispatcher()

    received = []

    def handler(tick):
        received.append(tick)

    dispatcher.register(handler)

    tick = {"ltp": 250}

    dispatcher.dispatch(tick)

    assert received[0] is tick


def test_dispatch_after_unregister_all():
    dispatcher = TickDispatcher()

    def handler(_):
        pass

    dispatcher.register(handler)
    dispatcher.unregister(handler)

    result = dispatcher.dispatch({"x": 1})

    assert result["failed"] == 0


def test_register_multiple_unique_handlers():
    dispatcher = TickDispatcher()

    count = []

    def h1(_):
        count.append(1)

    def h2(_):
        count.append(2)

    def h3(_):
        count.append(3)

    dispatcher.register(h1)
    dispatcher.register(h2)
    dispatcher.register(h3)

    dispatcher.dispatch({})

    assert count == [1, 2, 3]


def test_unregister_same_handler_twice():
    dispatcher = TickDispatcher()

    def handler(_):
        pass

    dispatcher.register(handler)

    dispatcher.unregister(handler)
    dispatcher.unregister(handler)

    result = dispatcher.dispatch({})

    assert result["failed"] == 0


def test_handler_exception_does_not_change_dispatch_result():
    dispatcher = TickDispatcher()

    def bad(_):
        raise Exception()

    dispatcher.register(bad)

    result = dispatcher.dispatch({"price": 1})

    assert result["dispatched"] is True
    assert result["failed"] == 1

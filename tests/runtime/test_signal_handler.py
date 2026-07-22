from runtime.signal_handler import SignalHandler


def test_signal_handler_initial_state():
    handler = SignalHandler()
    assert handler.signal_received is None


def test_register_signal():
    handler = SignalHandler()
    handler.register("SIGINT")
    assert handler.signal_received == "SIGINT"


def test_receive_sigint():
    handler = SignalHandler()
    handler.register("SIGINT")
    assert handler.is_shutdown_requested() is True


def test_receive_sigterm():
    handler = SignalHandler()
    handler.register("SIGTERM")
    assert handler.is_shutdown_requested() is True


def test_reset_signal():
    handler = SignalHandler()
    handler.register("SIGINT")
    handler.reset()
    assert handler.signal_received is None
from runtime.shutdown import Shutdown


def test_shutdown_closes_broker():
    shutdown = Shutdown()
    shutdown.close_broker()
    assert shutdown.broker_closed is True


def test_shutdown_flushes_logs():
    shutdown = Shutdown()
    shutdown.flush_logs()
    assert shutdown.logs_flushed is True


def test_shutdown_saves_state():
    shutdown = Shutdown()
    shutdown.save_state()
    assert shutdown.state_saved is True
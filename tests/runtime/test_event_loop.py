from runtime.event_loop import EventLoop


def test_event_loop_initial_state():
    loop = EventLoop()
    assert loop.running is False


def test_event_loop_start():
    loop = EventLoop()
    loop.start()
    assert loop.running is True


def test_event_loop_stop():
    loop = EventLoop()
    loop.start()
    loop.stop()
    assert loop.running is False


def test_event_loop_runs_iteration():
    loop = EventLoop()
    loop.run_iteration()
    assert loop.iterations == 1


def test_event_loop_iteration_count():
    loop = EventLoop()
    loop.run_iteration()
    loop.run_iteration()
    assert loop.iterations == 2
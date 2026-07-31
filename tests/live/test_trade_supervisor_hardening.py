from live.trade_supervisor import TradeSupervisor


def test_supervisor_start():
    supervisor = TradeSupervisor()

    supervisor.start()

    assert supervisor.is_running()


def test_supervisor_stop():
    supervisor = TradeSupervisor()

    supervisor.start()
    supervisor.stop()

    assert not supervisor.is_running()


def test_supervisor_pause():
    supervisor = TradeSupervisor()

    supervisor.pause()

    assert supervisor.is_paused()


def test_supervisor_resume():
    supervisor = TradeSupervisor()

    supervisor.pause()
    supervisor.resume()

    assert not supervisor.is_paused()


def test_supervisor_status():
    supervisor = TradeSupervisor()

    assert supervisor.status() is not None

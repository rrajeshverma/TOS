from runtime.lifecycle import Lifecycle


def test_startup_sequence():
    lifecycle = Lifecycle()
    lifecycle.start()
    assert lifecycle.state == "running"


def test_shutdown_sequence():
    lifecycle = Lifecycle()
    lifecycle.start()
    lifecycle.stop()
    assert lifecycle.state == "stopped"


def test_restart_sequence():
    lifecycle = Lifecycle()
    lifecycle.start()
    lifecycle.restart()
    assert lifecycle.state == "running"


def test_lifecycle_state_changes():
    lifecycle = Lifecycle()
    assert lifecycle.state == "created"
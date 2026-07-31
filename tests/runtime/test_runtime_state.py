from runtime.runtime_state import RuntimeState


def test_runtime_state_defaults():
    state = RuntimeState()
    assert state.status == "created"


def test_runtime_state_running():
    state = RuntimeState()
    state.running()
    assert state.status == "running"


def test_runtime_state_stopped():
    state = RuntimeState()
    state.stopped()
    assert state.status == "stopped"


def test_runtime_state_restart():
    state = RuntimeState()
    state.restart()
    assert state.status == "running"


def test_runtime_state_reset():
    state = RuntimeState()
    state.reset()
    assert state.status == "created"

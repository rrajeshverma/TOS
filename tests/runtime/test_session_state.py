from runtime.session_state import SessionState


def test_session_state_values():
    assert SessionState.PRE_OPEN == "PRE_OPEN"
    assert SessionState.OPEN == "OPEN"
    assert SessionState.CLOSED == "CLOSED"
    assert SessionState.HOLIDAY == "HOLIDAY"
    assert SessionState.MAINTENANCE == "MAINTENANCE"


def test_session_state_count():
    assert len(SessionState) == 5


def test_session_state_lookup():
    assert SessionState("OPEN") is SessionState.OPEN
    assert SessionState("CLOSED") is SessionState.CLOSED
    assert SessionState("HOLIDAY") is SessionState.HOLIDAY

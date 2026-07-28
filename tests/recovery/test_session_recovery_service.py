from recovery.session_recovery import (
    SessionRecoveryService,
)



def test_session_recovery_stores_session():

    recovery = SessionRecoveryService()


    result = recovery.recover(
        {
            "access_token": "TOKEN123",
        }
    )


    assert (
        result["access_token"]
        == "TOKEN123"
    )



def test_recovered_session_can_be_loaded():

    recovery = SessionRecoveryService()


    recovery.recover(
        {
            "access_token": "TOKEN123",
        }
    )


    session = recovery.get_session()


    assert session is not None

    assert (
        session["authenticated"]
        is True
    )



def test_authenticated_session_returns_true():

    recovery = SessionRecoveryService()


    recovery.recover(
        {
            "access_token": "TOKEN123",
        }
    )


    assert (
        recovery.is_authenticated()
        is True
    )



def test_missing_session_state_is_rejected():

    recovery = SessionRecoveryService()


    try:

        recovery.recover(
            {}
        )

        assert False

    except ValueError as exc:

        assert (
            str(exc)
            == "Session state required"
        )



def test_missing_token_is_rejected():

    recovery = SessionRecoveryService()


    try:

        recovery.recover(
            {
                "user": "demo",
            }
        )

        assert False

    except ValueError as exc:

        assert (
            str(exc)
            == "Access token required"
        )



def test_clear_removes_session():

    recovery = SessionRecoveryService()


    recovery.recover(
        {
            "access_token": "TOKEN123",
        }
    )


    recovery.clear()


    assert (
        recovery.get_session()
        is None
    )

    assert (
        recovery.is_authenticated()
        is False
    )

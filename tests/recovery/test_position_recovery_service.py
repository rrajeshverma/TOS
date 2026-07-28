from recovery.position_recovery import (
    PositionRecoveryService,
)



def test_position_recovery_stores_position():

    recovery = PositionRecoveryService()


    position = {
        "symbol": "NIFTY",
        "quantity": 65,
    }


    result = recovery.recover(
        position
    )


    assert (
        result["symbol"]
        == "NIFTY"
    )



def test_recovered_position_can_be_loaded():

    recovery = PositionRecoveryService()


    recovery.recover(
        {
            "symbol": "NIFTY",
            "quantity": 65,
        }
    )


    result = recovery.get(
        "NIFTY"
    )


    assert result is not None

    assert (
        result["quantity"]
        == 65
    )



def test_missing_position_returns_none():

    recovery = PositionRecoveryService()


    assert (
        recovery.get(
            "BANKNIFTY"
        )
        is None
    )



def test_multiple_positions_are_recovered():

    recovery = PositionRecoveryService()


    recovery.recover(
        {
            "symbol": "NIFTY",
            "quantity": 65,
        }
    )

    recovery.recover(
        {
            "symbol": "BANKNIFTY",
            "quantity": 15,
        }
    )


    assert (
        recovery.count()
        == 2
    )



def test_all_positions_returns_snapshot():

    recovery = PositionRecoveryService()


    recovery.recover(
        {
            "symbol": "NIFTY",
            "quantity": 65,
        }
    )


    positions = recovery.all_positions()


    assert len(positions) == 1



def test_invalid_position_is_rejected():

    recovery = PositionRecoveryService()


    try:

        recovery.recover(
            {
                "quantity": 65,
            }
        )

        assert False

    except ValueError as exc:

        assert (
            str(exc)
            == "Position symbol required"
        )

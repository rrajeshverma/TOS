from portfolio.position_sync_validator import (
    PositionSyncValidator,
)


class DummyPosition:

    def __init__(
        self,
        symbol="NIFTY",
        quantity=65,
    ):

        self.symbol = symbol
        self.quantity = quantity



def test_matching_positions_are_valid():

    validator = PositionSyncValidator()


    internal = DummyPosition()
    broker = DummyPosition()


    assert (
        validator.validate(
            internal,
            broker,
        )
        is True
    )



def test_symbol_mismatch_is_detected():

    validator = PositionSyncValidator()


    internal = DummyPosition(
        symbol="NIFTY"
    )

    broker = DummyPosition(
        symbol="BANKNIFTY"
    )


    assert (
        validator.validate(
            internal,
            broker,
        )
        is False
    )



def test_quantity_mismatch_is_detected():

    validator = PositionSyncValidator()


    internal = DummyPosition(
        quantity=65
    )

    broker = DummyPosition(
        quantity=130
    )


    assert (
        validator.validate(
            internal,
            broker,
        )
        is False
    )



def test_missing_internal_position_is_invalid():

    validator = PositionSyncValidator()


    assert (
        validator.validate(
            None,
            DummyPosition(),
        )
        is False
    )



def test_missing_broker_position_is_invalid():

    validator = PositionSyncValidator()


    assert (
        validator.validate(
            DummyPosition(),
            None,
        )
        is False
    )



def test_multiple_matching_positions():

    validator = PositionSyncValidator()


    positions = [
        (
            DummyPosition(
                "NIFTY",
                65,
            ),
            DummyPosition(
                "NIFTY",
                65,
            )
        ),
        (
            DummyPosition(
                "BANKNIFTY",
                15,
            ),
            DummyPosition(
                "BANKNIFTY",
                15,
            )
        ),
    ]


    for internal, broker in positions:

        assert (
            validator.validate(
                internal,
                broker,
            )
            is True
        )

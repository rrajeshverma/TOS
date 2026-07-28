"""
TOS Position Synchronization Validator

Validates internal positions against broker positions.
"""

from __future__ import annotations


class PositionSyncValidator:
    """
    Checks position consistency.
    """


    def validate(
        self,
        internal_position,
        broker_position,
    ) -> bool:
        """
        Return True when positions match.
        """

        if (
            internal_position is None
            or broker_position is None
        ):
            return False


        return (
            internal_position.symbol
            == broker_position.symbol
            and
            internal_position.quantity
            == broker_position.quantity
        )

"""
TOS Broker Confirmation Validator

Validates broker responses after order submission.
"""

from __future__ import annotations


class BrokerConfirmationValidator:
    """
    Validates broker order acknowledgement.
    """

    def is_confirmed(
        self,
        response,
    ) -> bool:
        """
        Return True when broker confirms order.
        """

        if response is None:
            return False

        if not isinstance(
            response,
            dict,
        ):
            return False

        status = response.get("status")

        order_id = response.get("orderId")

        return status == "success" and order_id is not None

"""
TOS Order Validator

Validates order safety before broker submission.
"""

from __future__ import annotations


class OrderValidator:
    """
    Validates trading order requests.
    """


    def validate(
        self,
        order,
    ) -> bool:
        """
        Return True when order is safe.
        """

        if order is None:
            return False


        if not hasattr(
            order,
            "symbol",
        ):
            return False


        if not hasattr(
            order,
            "quantity",
        ):
            return False


        if order.quantity <= 0:
            return False


        return True

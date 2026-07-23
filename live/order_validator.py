class OrderValidator:
    """
    Validates execution orders before broker submission.
    """

    REQUIRED_FIELDS = (
        "symbol",
        "quantity",
        "price",
    )

    def validate(
        self,
        order,
    ):
        if not isinstance(order, dict):
            return False

        for field in self.REQUIRED_FIELDS:
            if field not in order:
                return False

        if not isinstance(order["symbol"], str) or not order["symbol"].strip():
            return False

        if order["quantity"] <= 0:
            return False

        if order["price"] <= 0:
            return False

        return True

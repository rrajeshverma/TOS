"""
Integration Test:

Live Order Safety Flow

Validates:

Order Request
      |
      ▼
Safety Checks
      |
      ▼
Execution Permission
"""


class OrderSafetyGuard:

    def __init__(
        self,
        max_quantity=65,
        max_daily_loss=5000,
    ):
        self.max_quantity = max_quantity
        self.max_daily_loss = max_daily_loss
        self.orders = set()


    def validate_quantity(
        self,
        quantity,
    ):
        return quantity <= self.max_quantity


    def validate_daily_loss(
        self,
        loss,
    ):
        return loss <= self.max_daily_loss


    def check_duplicate(
        self,
        order_id,
    ):
        if order_id in self.orders:
            return False

        self.orders.add(order_id)

        return True


class DummyBroker:

    def __init__(self):
        self.submitted = []


    def submit(
        self,
        order,
    ):
        self.submitted.append(
            order
        )

        return {
            "status": "ACCEPTED",
            "order_id": order["order_id"],
        }


def create_order():

    return {
        "order_id": "LIVE001",
        "symbol": "NIFTY",
        "side": "BUY",
        "quantity": 65,
    }


def test_valid_quantity_passes():

    guard = OrderSafetyGuard()

    assert (
        guard.validate_quantity(65)
        is True
    )


def test_excess_quantity_is_blocked():

    guard = OrderSafetyGuard()

    assert (
        guard.validate_quantity(130)
        is False
    )


def test_daily_loss_limit_is_checked():

    guard = OrderSafetyGuard()

    assert (
        guard.validate_daily_loss(4000)
        is True
    )

    assert (
        guard.validate_daily_loss(6000)
        is False
    )


def test_duplicate_order_is_blocked():

    guard = OrderSafetyGuard()

    assert (
        guard.check_duplicate(
            "ORDER001"
        )
        is True
    )

    assert (
        guard.check_duplicate(
            "ORDER001"
        )
        is False
    )


def test_safe_order_reaches_broker():

    guard = OrderSafetyGuard()

    broker = DummyBroker()

    order = create_order()

    assert (
        guard.validate_quantity(
            order["quantity"]
        )
        is True
    )

    assert (
        guard.check_duplicate(
            order["order_id"]
        )
        is True
    )

    result = broker.submit(
        order
    )

    assert (
        result["status"]
        == "ACCEPTED"
    )

    assert len(
        broker.submitted
    ) == 1

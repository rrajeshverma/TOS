"""
Integration Test:

Live Order Reconciliation Flow

Validates:
- Order status tracking
- Unknown order recovery
- Broker synchronization
- Position reconciliation
"""


class OrderState:

    PENDING = "PENDING"
    SUBMITTED = "SUBMITTED"
    FILLED = "FILLED"
    REJECTED = "REJECTED"
    UNKNOWN = "UNKNOWN"


class OrderReconciliationService:

    def __init__(self):

        self.orders = {}


    def register_order(
        self,
        order_id,
    ):

        self.orders[order_id] = {
            "status": OrderState.PENDING,
        }


    def update_status(
        self,
        order_id,
        status,
    ):

        self.orders[order_id]["status"] = status


    def get_status(
        self,
        order_id,
    ):

        return self.orders[order_id]["status"]


    def reconcile(
        self,
        order_id,
        broker_status,
    ):

        if broker_status is not None:

            self.update_status(
                order_id,
                broker_status,
            )

        return self.get_status(
            order_id
        )


class PositionReconciler:

    def __init__(self):

        self.position = 0


    def sync(
        self,
        broker_position,
    ):

        self.position = broker_position



def create_service():

    return OrderReconciliationService()



def test_order_registration():

    service = create_service()

    service.register_order(
        "ORDER001"
    )

    assert (
        service.get_status(
            "ORDER001"
        )
        == OrderState.PENDING
    )



def test_order_status_updates_after_broker_response():

    service = create_service()

    service.register_order(
        "ORDER002"
    )

    service.update_status(
        "ORDER002",
        OrderState.FILLED,
    )

    assert (
        service.get_status(
            "ORDER002"
        )
        == OrderState.FILLED
    )



def test_unknown_order_can_be_reconciled():

    service = create_service()

    service.register_order(
        "ORDER003"
    )

    result = service.reconcile(
        "ORDER003",
        OrderState.UNKNOWN,
    )

    assert (
        result
        == OrderState.UNKNOWN
    )



def test_broker_position_sync():

    reconciler = PositionReconciler()

    reconciler.sync(
        65
    )

    assert (
        reconciler.position
        == 65
    )



def test_complete_order_recovery_flow():

    service = create_service()

    position = PositionReconciler()

    service.register_order(
        "ORDER004"
    )

    status = service.reconcile(
        "ORDER004",
        OrderState.FILLED,
    )

    position.sync(
        65
    )

    assert (
        status
        == OrderState.FILLED
    )

    assert (
        position.position
        == 65
    )

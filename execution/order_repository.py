class OrderRepository:
    """In-memory repository for orders."""

    def __init__(self):
        self._orders = {}

    def add(self, order):
        self._orders[order["order_id"]] = order

    def get(self, order_id):
        return self._orders.get(order_id)

class OrderRepository:
    """In-memory repository for orders."""

    def __init__(self):
        self._orders = {}

    def add(self, order):
        if hasattr(order, "order_id"):
            order_id = order.order_id
        elif isinstance(order, dict):
            order_id = order["order_id"]
        else:
            raise ValueError("Invalid order type")

        self._orders[order_id] = order

    def get(self, order_id):
        return self._orders.get(order_id)

    def exists(self, order_id) -> bool:
        return order_id in self._orders

    def remove(self, order_id):
        self._orders.pop(order_id, None)

    def all(self):
        return list(self._orders.values())

    @property
    def count(self):
        return len(self._orders)

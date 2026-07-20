class OrderService:
    """Coordinates broker order operations."""

    def __init__(self, broker, repository):
        self._broker = broker
        self._repository = repository

    def place_order(self, order):
        result = self._broker.place_order(order)
        self._repository.add(result)
        return result

class OrderRouter:
    def __init__(self, broker):
        self.broker = broker

    def place_order(self, order):
        return self.broker.place_order(order)

    def modify_order(self, order_id, **kwargs):
        return self.broker.modify_order(
            order_id,
            **kwargs,
        )

    def cancel_order(self, order_id):
        return self.broker.cancel_order(order_id)

    def order_status(self, order_id):
        return self.broker.get_order(order_id)

    def order_history(self):
        return self.broker.get_orders()

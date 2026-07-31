class Broker:
    def place_order(self, order):
        raise NotImplementedError

    def cancel_order(self, order_id):
        raise NotImplementedError

    def modify_order(self, order_id, order):
        raise NotImplementedError

    def positions(self):
        raise NotImplementedError

    def orders(self):
        raise NotImplementedError

    def holdings(self):
        raise NotImplementedError

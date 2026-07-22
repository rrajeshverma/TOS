class BrokerRouter:

    def __init__(self, broker):
        self.broker = broker

    def route_market_data(self):
        return []

    def route_order(self, order):
        return self.broker.place_order(order)

    def route_positions(self):
        return self.broker.get_positions()

    def route_account(self):
        return self.broker.get_funds()

    def health(self):
        return self.broker.is_connected()
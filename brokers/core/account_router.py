class AccountRouter:

    def __init__(self, broker):
        self.broker = broker

    def fetch_balance(self):
        return self.broker.get_funds()

    def fetch_positions(self):
        return self.broker.get_positions()

    def fetch_holdings(self):
        return self.broker.get_holdings()

    def margin_information(self):
        return self.broker.get_funds()

    def summary(self):
        funds = self.fetch_balance()

        return {
            "funds": funds,
            "positions": self.fetch_positions(),
            "holdings": self.fetch_holdings(),
        }
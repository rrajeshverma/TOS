class PaperPortfolio:
    def __init__(self, initial_cash=1_000_000):
        self.cash = initial_cash
        self._positions = {}

    def buy(self, symbol, quantity, price):
        if quantity <= 0:
            raise ValueError("quantity must be positive")

        if price <= 0:
            raise ValueError("price must be positive")

        self.cash -= quantity * price
        self._positions[symbol] = self._positions.get(symbol, 0) + quantity

    def sell(self, symbol, quantity, price):
        if quantity <= 0:
            raise ValueError("quantity must be positive")

        if price <= 0:
            raise ValueError("price must be positive")

        self.cash += quantity * price
        self._positions[symbol] = self._positions.get(symbol, 0) - quantity

    def position(self, symbol):
        return self._positions.get(symbol, 0)

    def positions(self):
        return dict(self._positions)

    def equity(self):
        return self.cash

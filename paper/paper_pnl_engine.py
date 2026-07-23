class PaperPnLEngine:
    def __init__(self):
        self.realized_pnl = 0
        self.unrealized_pnl = 0
        self._positions = {}

    def buy(self, symbol, quantity, price):
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        if price <= 0:
            raise ValueError("price must be positive")

        self._positions[symbol] = {
            "quantity": quantity,
            "price": price,
        }

    def sell(self, symbol, quantity, price):
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        if price <= 0:
            raise ValueError("price must be positive")

        position = self._positions.get(symbol)
        if position is None:
            return

        self.realized_pnl += (price - position["price"]) * quantity

    def mark_to_market(self, symbol, market_price):
        position = self._positions.get(symbol)
        if position is None:
            return 0

        return (market_price - position["price"]) * position["quantity"]

    def positions(self):
        return self._positions

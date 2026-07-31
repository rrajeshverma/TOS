class PaperPositionBook:
    def __init__(self):
        self._positions = {}

    def record(self, trade):
        if trade is None:
            raise ValueError("trade cannot be None")

        symbol = trade["symbol"]
        quantity = trade["quantity"]
        price = trade["price"]

        if trade["side"] == "SELL":
            quantity = -quantity

        if symbol not in self._positions:
            self._positions[symbol] = {
                "symbol": symbol,
                "quantity": 0,
                "price": price,
            }

        self._positions[symbol]["quantity"] += quantity
        self._positions[symbol]["price"] = price

    def get(self, symbol):
        return self._positions.get(symbol)

    def positions(self):
        return list(self._positions.values())

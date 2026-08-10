class SimpleStrategy:
    def __init__(self):
        self.last_price = None

    def should_enter(self, price):
        """
        Simple breakout logic:
        - If price moves up → BUY
        - If price moves down → SELL
        """

        if self.last_price is None:
            self.last_price = price
            return None

        if price > self.last_price:
            signal = "BUY"
        elif price < self.last_price:
            signal = "SELL"
        else:
            signal = None

        self.last_price = price
        return signal

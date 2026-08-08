from decimal import Decimal


class MarketTick:
    def __init__(self, symbol, ltp, timestamp, volume=None):
        self.symbol = symbol
        self.ltp = Decimal(ltp) if ltp is not None else None
        self.timestamp = timestamp
        self.volume = volume

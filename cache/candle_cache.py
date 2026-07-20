class CandleCache:
    def __init__(self):
        self._cache = {}

    def set(self, symbol: str, candle: dict) -> None:
        self._cache[symbol] = candle

    def get(self, symbol: str):
        return self._cache.get(symbol)

    def clear(self) -> None:
        self._cache.clear()

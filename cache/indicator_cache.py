class IndicatorCache:
    def __init__(self):
        self._cache = {}

    def set(self, symbol: str, indicator: str, value):
        self._cache.setdefault(symbol, {})
        self._cache[symbol][indicator] = value

    def get(self, symbol: str, indicator: str):
        return self._cache.get(symbol, {}).get(indicator)

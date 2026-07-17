class HistoricalDataFeed:
    def __init__(self, candles):
        self._candles = list(candles)
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if not self.has_next():
            raise StopIteration

        return self.next()

    def has_next(self):
        return self._index < len(self._candles)

    def next(self):
        if not self.has_next():
            raise StopIteration("No more candles available.")

        candle = self._candles[self._index]
        self._index += 1
        return candle

    def peek(self):
        if not self.has_next():
            raise StopIteration("No more candles available.")

        return self._candles[self._index]

    def current_index(self):
        return self._index

    def reset(self):
        self._index = 0
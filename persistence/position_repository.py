class PositionRepository:
    def __init__(self):
        self._positions = {}

    def add(self, position: dict) -> None:
        self._positions[position["symbol"]] = position

    def get(self, symbol: str):
        return self._positions.get(symbol)

    def get_all(self):
        return list(self._positions.values())

    def remove(self, symbol: str) -> None:
        self._positions.pop(symbol, None)

    def has_position(self, symbol: str) -> bool:
        return symbol in self._positions

    def count(self) -> int:
        return len(self._positions)

    def clear(self) -> None:
        self._positions.clear()

    def update(self, position: dict) -> None:
        self._positions[position["symbol"]] = position
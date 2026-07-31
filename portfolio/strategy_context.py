class StrategyContext:
    def __init__(self):
        self._data = {}

    def set(
        self,
        key,
        value,
    ):
        self._data[key] = value

    def get(
        self,
        key,
        default=None,
    ):
        return self._data.get(
            key,
            default,
        )

    def contains(
        self,
        key,
    ):
        return key in self._data

    def remove(
        self,
        key,
    ):
        self._data.pop(
            key,
            None,
        )

    def clear(
        self,
    ):
        self._data.clear()

    def keys(
        self,
    ):
        return list(self._data.keys())

    def values(
        self,
    ):
        return list(self._data.values())

    def items(
        self,
    ):
        return list(self._data.items())

    def size(
        self,
    ):
        return len(self._data)

    def is_empty(
        self,
    ):
        return self.size() == 0

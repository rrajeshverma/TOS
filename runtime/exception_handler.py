"""
Exception handling utilities.
"""


class ExceptionHandler:
    """Collects runtime exceptions."""

    def __init__(self) -> None:
        self._exceptions = []

    @property
    def count(self) -> int:
        return len(self._exceptions)

    def record(self, exception: Exception) -> None:
        self._exceptions.append(exception)

    def last_exception(self):
        if not self._exceptions:
            return None
        return self._exceptions[-1]

    def clear(self) -> None:
        self._exceptions.clear()
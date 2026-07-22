from __future__ import annotations

from domain.market import Market


class MarketHistory:
    """
    Maintains completed market candles
    for indicator calculations.
    """

    def __init__(
        self,
        max_size: int | None = None,
    ):
        self._history: list[Market] = []
        self.max_size = max_size


    def add(
        self,
        market: Market,
    ) -> None:

        if market is None:
            raise ValueError(
                "Market cannot be None."
            )

        self._history.append(
            market
        )

        if (
            self.max_size is not None
            and len(self._history) > self.max_size
        ):
            self._history.pop(0)


    def get(self) -> list[Market]:
        """
        Return market history copy.
        """

        return list(
            self._history
        )


    def count(self) -> int:
        return len(
            self._history
        )


    def latest(self) -> Market | None:
        if not self._history:
            return None

        return self._history[-1]


    def clear(self) -> None:
        self._history.clear()

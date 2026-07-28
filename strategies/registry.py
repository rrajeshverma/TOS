"""
TOS Strategy Registry

Manages strategy plugins dynamically.
"""

from __future__ import annotations


class StrategyRegistry:
    """
    Registry for strategy plugins.
    """

    def __init__(self) -> None:

        self._strategies: dict[str, object] = {}


    def register(
        self,
        name: str,
        strategy: object,
    ) -> None:
        """
        Register a strategy.
        """

        if not name:
            raise ValueError(
                "Strategy name is required"
            )

        if strategy is None:
            raise ValueError(
                "Strategy object is required"
            )

        self._strategies[name] = strategy


    def get(
        self,
        name: str,
    ):
        """
        Retrieve strategy by name.
        """

        return self._strategies.get(
            name
        )


    def list(
        self,
    ) -> list[str]:
        """
        List registered strategies.
        """

        return list(
            self._strategies.keys()
        )


    def remove(
        self,
        name: str,
    ) -> None:
        """
        Remove strategy.
        """

        self._strategies.pop(
            name,
            None,
        )

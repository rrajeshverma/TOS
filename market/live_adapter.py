"""
TOS Live Market Adapter Interface

Broker-independent live market data adapter.
"""

from __future__ import annotations


class LiveMarketAdapter:
    """
    Live market data connection lifecycle.
    """

    def __init__(self) -> None:

        self._status = "DISCONNECTED"
        self._subscriptions: set[str] = set()


    def connect(
        self,
    ) -> None:
        """
        Connect to live market feed.
        """

        self._status = "CONNECTED"


    def disconnect(
        self,
    ) -> None:
        """
        Disconnect from live market feed.
        """

        self._status = "DISCONNECTED"


    def status(
        self,
    ) -> str:
        """
        Return adapter connection status.
        """

        return self._status


    def subscribe(
        self,
        symbol: str,
    ) -> None:
        """
        Subscribe to market symbol.
        """

        if not symbol:
            raise ValueError(
                "Symbol is required"
            )

        self._subscriptions.add(
            symbol
        )


    def subscriptions(
        self,
    ) -> set[str]:
        """
        Return subscribed symbols.
        """

        return set(
            self._subscriptions
        )

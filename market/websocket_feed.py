from __future__ import annotations


class WebSocketFeed:
    """
    Market websocket feed abstraction.

    Handles:
    - connection state
    - subscriptions
    - tick forwarding
    """

    def __init__(
        self,
        dispatcher=None,
    ):
        self._connected = False
        self._subscriptions = set()
        self.dispatcher = dispatcher

    def connect(self):
        self._connected = True

    def disconnect(self):
        self._connected = False

    def is_connected(self):
        return self._connected

    def subscribe(
        self,
        symbol,
    ):
        self._subscriptions.add(symbol)

    def unsubscribe(
        self,
        symbol,
    ):
        self._subscriptions.discard(symbol)

    @property
    def subscriptions(self):
        return set(self._subscriptions)

    def receive_tick(
        self,
        tick,
    ):
        """
        Receive broker tick and forward to dispatcher.
        """

        if tick is None:
            raise ValueError("Tick cannot be None.")

        if self.dispatcher is not None:
            self.dispatcher(tick)

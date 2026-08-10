from __future__ import annotations

from collections.abc import Callable
from decimal import Decimal

from domain.market_tick import MarketTick


class MarketDataService:
    def __init__(self, websocket=None):  # ✅ FIXED
        self.websocket = websocket
        self._connected = True
        self._subscriptions: set[str] = set()
        self.tick_callback: Callable | None = None

    # ---------------- CONNECTION ----------------

    @property
    def is_connected(self) -> bool:
        return self._connected

    def connect(self) -> None:
        self._connected = True
        if self.websocket:
            self.websocket.connect()

    def disconnect(self) -> None:
        self._connected = False
        if self.websocket:
            self.websocket.disconnect()

    # ---------------- SUBSCRIPTIONS ----------------

    def subscribe(self, instruments):
        for i in instruments:
            symbol = i[1] if isinstance(i, tuple) else i
            self._subscriptions.add(symbol)

        if self.websocket:
            self.websocket.subscribe(instruments)

    def unsubscribe(self, instruments):
        original = instruments

        if isinstance(instruments, str):
            instruments = [instruments]

        for i in instruments:
            symbol = i[1] if isinstance(i, tuple) else i
            self._subscriptions.discard(symbol)

        if self.websocket:
            self.websocket.unsubscribe(original)

    def clear_subscriptions(self):
        self._subscriptions.clear()

        if self.websocket:
            self.websocket.clear_subscriptions()

    @property
    def subscriptions(self):
        if self.websocket and hasattr(self.websocket, "subscriptions"):
            return self.websocket.subscriptions
        return self._subscriptions

    # ---------------- CALLBACK ----------------

    def register_tick_callback(self, callback: Callable):
        self.tick_callback = callback

        if self.websocket:
            self.websocket.register_tick_callback(callback)

    # ---------------- TICK ----------------

    def to_market_tick(self, data):
        if isinstance(data, dict):
            return MarketTick(
                symbol=data["symbol"],
                ltp=Decimal(str(data["ltp"])),
                timestamp=data.get("timestamp"),
                volume=data.get("volume"),
            )

        return MarketTick(
            symbol=data.symbol,
            ltp=Decimal(str(data.ltp)),
            timestamp=getattr(data, "timestamp", None),
            volume=getattr(data, "volume", None),
        )

    # ---------------- EMIT ----------------

    def emit_market_tick(self, data):
        tick = self.to_market_tick(data)

        # ✅ FIRST: local callback (tests use this)
        if callable(self.tick_callback):
            self.tick_callback(tick)
            return

        # ✅ SECOND: websocket callback
        if self.websocket:
            callback = getattr(self.websocket, "tick_callback", None)
            if callable(callback):
                callback(tick)

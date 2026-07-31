class BrokerSession:
    """
    Manages the lifecycle of a broker session.

    Supports both:
    - Legacy API:
        connect(), disconnect(), reconnect(), reset(),
        is_connected(), status()
    - Newer API:
        start(), stop(), restart(), is_active()
    """

    def __init__(self, broker=None):
        self._broker = broker
        self._connected = False

    # ---------------------------------------------------------
    # Legacy API
    # ---------------------------------------------------------

    def connect(self):
        """Connect to the broker."""
        if self._broker is not None:
            self._broker.connect()

        self._connected = True

    def disconnect(self):
        """Disconnect from the broker."""
        if self._broker is not None:
            self._broker.disconnect()

        self._connected = False

    def reconnect(self):
        """Reconnect to the broker."""
        self.disconnect()
        self.connect()

    def reset(self):
        """Reset the session."""
        self.disconnect()

    def is_connected(self):
        """Return True if connected."""
        return self._connected

    def status(self):
        """Return session status."""
        return {
            "connected": self._connected,
            "broker": (
                type(self._broker).__name__ if self._broker is not None else None
            ),
        }

    # ---------------------------------------------------------
    # Compatibility API
    # ---------------------------------------------------------

    def start(self):
        """Alias for connect()."""
        self.connect()

    def stop(self):
        """Alias for disconnect()."""
        self.disconnect()

    def restart(self):
        """Alias for reconnect()."""
        self.reconnect()

    def is_active(self):
        """Alias for is_connected()."""
        return self.is_connected()

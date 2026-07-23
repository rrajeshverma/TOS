class ReconnectManager:
    """
    Manages market data reconnection attempts.
    """

    def __init__(self):
        self._connected = False
        self._retry_count = 0

    def connect(self):
        self._connected = True

    def disconnect(self):
        self._connected = False

    def reconnect(self):
        self.disconnect()
        self._retry_count += 1
        self.connect()

    def is_connected(self):
        return self._connected

    def retry_count(self):
        return self._retry_count

    def reset(self):
        self._connected = False
        self._retry_count = 0

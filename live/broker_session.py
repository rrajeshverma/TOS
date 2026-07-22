class BrokerSession:
    """
    Manages broker connection lifecycle.
    """

    def __init__(self):
        self._connected = False


    def connect(self):
        self._connected = True



    def disconnect(self):
        self._connected = False



    def reconnect(self):
        self.disconnect()
        self.connect()



    def reset(self):
        self._connected = False



    def is_connected(self):
        return self._connected



    def status(self):
        """
        Returns current broker session health.
        """

        return {
            "connected": self._connected,
        }
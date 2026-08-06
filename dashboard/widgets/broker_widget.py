"""
Broker Dashboard Widget.
"""


class BrokerWidget:
    """
    Displays broker connection information.
    """

    def __init__(
        self,
        connected=False,
        broker="DHAN",
        latency_ms=0,
        heartbeat="UNKNOWN",
    ) -> None:
        self.connected = connected
        self.broker = broker
        self.latency_ms = latency_ms
        self.heartbeat = heartbeat

    def render(self) -> str:
        """
        Render broker information.
        """

        status = "CONNECTED" if self.connected else "DISCONNECTED"

        return (
            "Broker\n"
            f"Status    : {status}\n"
            f"Broker    : {self.broker}\n"
            f"Latency   : {self.latency_ms} ms\n"
            f"Heartbeat : {self.heartbeat}\n"
        )

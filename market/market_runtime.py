class MarketRuntime:
    """
    Coordinates live market data processing.

    Responsibilities:
    - Receive market feed dependency
    - Manage market runtime lifecycle
    """

    def __init__(
        self,
        feed=None,
    ):
        self.feed = feed
        self.running = False

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def is_running(self):
        return self.running

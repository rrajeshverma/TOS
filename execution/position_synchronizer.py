class PositionSynchronizer:
    """Synchronizes broker positions with TOS."""

    def __init__(self, broker):
        self.broker = broker

    def sync(self):
        """Fetch positions from broker."""
        return self.broker.get_positions()
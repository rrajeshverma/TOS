"""
Runtime recovery manager.
"""


class RecoveryManager:
    """Coordinates runtime recovery after failures."""

    def __init__(self, broker):
        self._broker = broker

    def recover(self):
        """Recover runtime state."""
        return {
            "orders": self._broker.get_orders(),
            "positions": self._broker.get_positions(),
            "holdings": self._broker.get_holdings(),
            "funds": self._broker.get_funds(),
        }

"""
Portfolio reconciliation service.
"""


class ReconciliationService:
    """Compares broker and local positions."""

    def reconcile(self, broker_positions, local_positions):
        differences = []

        broker = {p.symbol: p.quantity for p in broker_positions}
        local = {p.symbol: p.quantity for p in local_positions}

        symbols = set(broker) | set(local)

        for symbol in symbols:
            if broker.get(symbol, 0) != local.get(symbol, 0):
                differences.append(
                    {
                        "symbol": symbol,
                        "broker": broker.get(symbol, 0),
                        "local": local.get(symbol, 0),
                    }
                )

        return differences

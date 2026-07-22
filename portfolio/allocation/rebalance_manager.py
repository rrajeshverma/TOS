from datetime import datetime


class RebalanceManager:
    """
    Handles portfolio allocation rebalancing decisions.
    """

    def __init__(self, threshold=10):
        self.threshold = threshold
        self.history = []


    def should_rebalance(
        self,
        current_allocation,
        target_allocation,
    ):

        difference = abs(
            current_allocation - target_allocation
        )

        return difference >= self.threshold


    def rebalance(
        self,
        current_allocation,
        target_allocation,
    ):

        event = {
            "from": current_allocation,
            "to": target_allocation,
            "timestamp": datetime.now(),
        }

        self.history.append(event)

        return event


    def rebalance_count(self):

        return len(self.history)


    def last_rebalance(self):

        if not self.history:
            return None

        return self.history[-1]


    def report(self):

        return {
            "threshold": self.threshold,
            "rebalance_count": len(self.history),
            "history": self.history,
        }
from strategy.orb_strategy import OrbStrategy


class StrategyFactory:
    """Creates strategy instances."""

    def create(self, name):
        if name == "ORB":
            return OrbStrategy()

        raise ValueError(f"Unknown strategy: {name}")

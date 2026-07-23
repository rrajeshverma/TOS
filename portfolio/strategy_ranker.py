class StrategyRanker:
    """
    Ranks trading strategies based on performance score.
    """

    def __init__(self):
        self.scores = {}

    def add_strategy(
        self,
        name,
        score,
    ):
        self.scores[name] = score

    def remove_strategy(
        self,
        name,
    ):
        self.scores.pop(name, None)

    def get_score(
        self,
        name,
    ):
        return self.scores.get(name, 0)

    def rank(self):
        return sorted(
            self.scores.items(),
            key=lambda item: item[1],
            reverse=True,
        )

    def best_strategy(self):
        ranked = self.rank()

        if not ranked:
            return None

        return ranked[0][0]

    def count(self):
        return len(self.scores)

    def summary(self):
        return {
            "strategies": self.count(),
            "ranking": self.rank(),
            "best": self.best_strategy(),
        }

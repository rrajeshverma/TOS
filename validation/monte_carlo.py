import random


class MonteCarlo:
    def __init__(
        self,
        simulations=1000,
        seed=None,
    ):
        self.simulations = simulations
        self.random = random.Random(seed)

    def run(self, trades):
        if not trades:
            return []

        if self.simulations <= 0:
            return []

        results = []

        for _ in range(self.simulations):
            shuffled = list(trades)

            self.random.shuffle(shuffled)

            results.append(sum(shuffled))

        return results

    def run(self, trades):
        if not trades:
            return []

        if self.simulations <= 0:
            return []

        results = []

        for _ in range(self.simulations):
            shuffled = list(trades)

            self.random.shuffle(shuffled)

            results.append(sum(shuffled))

        return results

class Robustness:
    def evaluate(self, results):
        if not results:
            return 0.0

        if len(results) == 1:
            return 1.0

        profits = [r.net_profit for r in results]

        mean = sum(profits) / len(profits)

        if mean == 0:
            return 0.0

        variance = sum((p - mean) ** 2 for p in profits) / len(profits)
        std = variance ** 0.5

        cv = abs(std / mean)

        return max(0.0, min(1.0, 1.0 / (1.0 + cv)))
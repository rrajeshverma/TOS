class WindowGenerator:
    def __init__(self, training_size, testing_size):
        self.training_size = training_size
        self.testing_size = testing_size

    def generate(self, candles):
        windows = []

        total = self.training_size + self.testing_size

        if len(candles) < total:
            return windows

        start = 0

        while start + total <= len(candles):
            train = candles[
                start:start + self.training_size
            ]

            test = candles[
                start + self.training_size:
                start + total
            ]

            windows.append((train, test))

            start += self.testing_size

        return windows
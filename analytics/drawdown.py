class Drawdown:
    def __init__(self):
        self.max_drawdown = 0
        self.duration = 0
        self.max_duration = 0

    def calculate(self, current_equity, peak_equity):
        return peak_equity - current_equity

    def calculate_percentage(self, current_equity, peak_equity):
        if peak_equity == 0:
            return 0.0

        return (self.calculate(current_equity, peak_equity) / peak_equity) * 100

    def update(self, current_equity, peak_equity):
        drawdown = self.calculate(current_equity, peak_equity)

        self.max_drawdown = max(self.max_drawdown, drawdown)

        if drawdown > 0:
            self.duration += 1
            self.max_duration = max(self.max_duration, self.duration)
        else:
            self.duration = 0

        return drawdown

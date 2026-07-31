class DrawdownAnalyzer:
    def __init__(self, equity_curve):
        if not equity_curve:
            self.max_drawdown = 0
            self.current_drawdown = 0
            return

        peak = equity_curve[0]
        self.max_drawdown = 0

        for value in equity_curve:
            peak = max(peak, value)
            self.max_drawdown = max(
                self.max_drawdown,
                peak - value,
            )

        self.current_drawdown = peak - equity_curve[-1]

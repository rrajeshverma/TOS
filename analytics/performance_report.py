from analytics.returns import Returns
from analytics.statistics import Statistics


class PerformanceReport:
    def __init__(self):
        self.returns = Returns()
        self.statistics = Statistics()

    def generate(
        self,
        initial_capital,
        ending_capital,
        years,
        trades,
        max_drawdown_percent=0.0,
        returns_series=None,
    ):
        if returns_series is None:
            returns_series = []

        cagr = self.returns.cagr(
            ending_capital,
            initial_capital,
            years,
        )

        return {
            "initial_capital": initial_capital,
            "ending_capital": ending_capital,
            "total_trades": len(trades),
            "total_return": self.returns.calculate(
                ending_capital,
                initial_capital,
            ),
            "cagr": cagr,
            "win_rate": self.statistics.win_rate(trades),
            "profit_factor": self.statistics.profit_factor(trades),
            "payoff_ratio": self.statistics.payoff_ratio(trades),
            "expectancy": self.statistics.expectancy(trades),
            "recovery_factor": self.statistics.recovery_factor(
                ending_capital - initial_capital,
                max_drawdown_percent,
            ),
            "sharpe_ratio": self.statistics.sharpe_ratio(
                returns_series,
            ),
            "sortino_ratio": self.statistics.sortino_ratio(
                returns_series,
            ),
            "calmar_ratio": self.statistics.calmar_ratio(
                cagr,
                max_drawdown_percent,
            ),
        }
from analytics.backtest_summary import BacktestSummary


class PerformanceDashboard:
    def __init__(self, initial_capital, trades):
        summary = BacktestSummary(
            initial_capital=initial_capital,
            trades=trades,
        )

        self.metrics = {
            "initial_capital": summary.initial_capital,
            "final_capital": summary.final_capital,
            "net_profit": summary.net_profit,
            "win_rate": summary.win_rate,
            "profit_factor": summary.profit_factor,
            "total_trades": summary.total_trades,
        }

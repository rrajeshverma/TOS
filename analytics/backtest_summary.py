from analytics.trade_performance_report import TradePerformanceReport
from analytics.trade_statistics import TradeStatistics


class BacktestSummary:
    def __init__(self, initial_capital, trades):
        performance = TradePerformanceReport(trades)
        statistics = TradeStatistics(trades)

        self.initial_capital = initial_capital
        self.total_trades = performance.total_trades
        self.net_profit = performance.net_profit
        self.win_rate = performance.win_rate
        self.profit_factor = statistics.profit_factor

        self.final_capital = initial_capital + self.net_profit

from analytics.performance_metrics import PerformanceMetrics


class PerformanceSummary:
    def generate(self, trades):
        return {
            "total_return": PerformanceMetrics.total_return(trades),
            "average_trade": PerformanceMetrics.average_trade(trades),
            "best_trade": PerformanceMetrics.best_trade(trades),
            "worst_trade": PerformanceMetrics.worst_trade(trades),
            "win_rate": PerformanceMetrics.win_rate(trades),
        }

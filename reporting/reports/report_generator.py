from reporting.models.performance_model import PerformanceModel
from reporting.reports.performance_report import PerformanceReport


class ReportGenerator:
    """Generates performance reports."""

    def generate(
        self,
        performance: PerformanceModel,
    ) -> PerformanceReport:

        summary = (
        "Trades\n"
        "--------------------\n"
        f"Total Trades: {performance.total_trades}\n"
        f"Winning Trades: {performance.winning_trades}\n"
        f"Losing Trades: {performance.losing_trades}\n\n"

        "Profit\n"
        "--------------------\n"
        f"Gross Profit: {performance.gross_profit}\n"
        f"Gross Loss: {performance.gross_loss}\n"
        f"Net Profit: {performance.net_profit}\n\n"

        "Performance\n"
        "--------------------\n"
        f"Win Rate: {performance.win_rate}\n"
        f"Profit Factor: {performance.profit_factor}\n"
        f"Expectancy: {performance.expectancy}\n"
        f"Recovery Factor: {performance.recovery_factor}\n\n"

        "Risk\n"
        "--------------------\n"
        f"Peak Equity: {performance.peak_equity}\n"
        f"Maximum Drawdown: {performance.max_drawdown}\n"
        f"Maximum Drawdown %: {performance.max_drawdown_percent}\n\n"

        "Streaks\n"
        "--------------------\n"
        f"Maximum Consecutive Wins: "
        f"{performance.max_consecutive_wins}\n"
        f"Maximum Consecutive Losses: "
        f"{performance.max_consecutive_losses}"
    )

        return PerformanceReport(
            performance=performance,
            summary=summary,
        )
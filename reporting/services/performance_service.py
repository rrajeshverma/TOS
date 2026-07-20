from reporting.models.performance_model import PerformanceModel
from reporting.reports.trade_statistics import TradeStatistics
from reporting.reports.equity_curve import EquityCurve
from reporting.reports.drawdown import Drawdown

class PerformanceService:
    """Service for calculating trading performance metrics."""

    def calculate(self, trades: list) -> PerformanceModel:
        stats = TradeStatistics()
        equity_curve = EquityCurve()
        drawdown = Drawdown()
        model = PerformanceModel()

        # Trade counts
        model.total_trades = stats.total_trades(trades)
        model.winning_trades = stats.winning_trades(trades)
        model.losing_trades = stats.losing_trades(trades)

        # Profit metrics
        model.gross_profit = stats.gross_profit(trades)

        model.gross_loss = stats.gross_loss(trades)

        model.net_profit = sum(
            trade.pnl
            for trade in trades
        )

        # Win Statistics
        model.win_rate = stats.win_rate(trades)

        model.profit_factor = stats.profit_factor(trades)

        # Trade Statistics
        model.average_win = stats.average_win(trades)

        model.average_loss = stats.average_loss(trades)

        model.largest_win = stats.largest_win(trades)

        model.largest_loss = stats.largest_loss(trades)

        # Expectancy
        model.expectancy = stats.expectancy(trades)

        # Equity Curve
        model.equity_curve = equity_curve.build(
            [trade.pnl for trade in trades]
        )

        # Maximum Drawdown
        model.max_drawdown = drawdown.calculate(
            model.equity_curve
        )

        # Peak Equity
        if model.equity_curve:
            model.peak_equity = max(
                model.equity_curve
            )

        # Maximum Drawdown %
        if model.peak_equity > 0:
            model.max_drawdown_percent = (
                model.max_drawdown
                / model.peak_equity
            ) * 100

        # Recovery Factor
        if model.max_drawdown > 0:
            model.recovery_factor = (
                model.net_profit
                / model.max_drawdown
            )

        from reporting.reports.streak_statistics import (
            StreakStatistics,
        )

        streaks = StreakStatistics()

        model.max_consecutive_wins = (
            streaks.max_consecutive_wins(trades)
        )

        model.max_consecutive_losses = (
            streaks.max_consecutive_losses(trades)
        )

        return model

    def _calculate_trade_counts(
        self,
        model: PerformanceModel,
        trades: list,
    ) -> None:
        """Calculate trade count statistics."""

        model.total_trades = len(trades)

        model.winning_trades = sum(
            1
            for trade in trades
            if trade.pnl > 0
        )

        model.losing_trades = sum(
            1
            for trade in trades
            if trade.pnl < 0
        )
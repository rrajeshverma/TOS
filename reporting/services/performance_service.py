from reporting.models.performance_model import PerformanceModel


class PerformanceService:
    """Service for calculating trading performance metrics."""

    def calculate(self, trades: list) -> PerformanceModel:
        model = PerformanceModel()

        # Trade counts
        self._calculate_trade_counts(model, trades)

        # Profit metrics
        model.gross_profit = sum(trade.pnl for trade in trades if trade.pnl > 0)

        model.gross_loss = abs(sum(trade.pnl for trade in trades if trade.pnl < 0))

        model.net_profit = sum(trade.pnl for trade in trades)

        # Win rate
        if model.total_trades > 0:
            model.win_rate = (model.winning_trades / model.total_trades) * 100

        # Profit factor
        if model.gross_loss > 0:
            model.profit_factor = model.gross_profit / model.gross_loss

        # Average & largest trade statistics
        winning_trades = [trade.pnl for trade in trades if trade.pnl > 0]

        losing_trades = [trade.pnl for trade in trades if trade.pnl < 0]

        if winning_trades:
            model.average_win = sum(winning_trades) / len(winning_trades)
            model.largest_win = max(winning_trades)

        if losing_trades:
            model.average_loss = abs(sum(losing_trades) / len(losing_trades))
            model.largest_loss = abs(min(losing_trades))

        # Expectancy
        if model.total_trades > 0:
            win_probability = model.winning_trades / model.total_trades

            loss_probability = model.losing_trades / model.total_trades

            model.expectancy = (win_probability * model.average_win) - (
                loss_probability * model.average_loss
            )

        # Equity curve
        running_equity = 0.0

        for trade in trades:
            running_equity += trade.pnl
            model.equity_curve.append(running_equity)

        # Maximum Drawdown
        peak = 0.0

        for equity in model.equity_curve:
            peak = max(peak, equity)
            drawdown = peak - equity

            model.max_drawdown = max(
                model.max_drawdown,
                drawdown,
            )

        # Peak Equity
        if model.equity_curve:
            model.peak_equity = max(model.equity_curve)

        # Maximum Drawdown Percentage
        if model.equity_curve:
            peak_equity = max(model.equity_curve)

            if peak_equity > 0:
                model.max_drawdown_percent = (model.max_drawdown / peak_equity) * 100

        # Recovery Factor
        if model.max_drawdown > 0:
            model.recovery_factor = model.net_profit / model.max_drawdown

        # Maximum Consecutive Wins
        current_wins = 0

        for trade in trades:
            if trade.pnl > 0:
                current_wins += 1
                model.max_consecutive_wins = max(
                    model.max_consecutive_wins,
                    current_wins,
                )
            else:
                current_wins = 0

            # Maximum Consecutive Losses
            current_losses = 0

            for trade in trades:
                if trade.pnl < 0:
                    current_losses += 1

                    model.max_consecutive_losses = max(
                        model.max_consecutive_losses,
                        current_losses,
                    )
                else:
                    current_losses = 0

        return model

    def _calculate_trade_counts(
        self,
        model: PerformanceModel,
        trades: list,
    ) -> None:
        """Calculate trade count statistics."""

        model.total_trades = len(trades)

        model.winning_trades = sum(1 for trade in trades if trade.pnl > 0)

        model.losing_trades = sum(1 for trade in trades if trade.pnl < 0)

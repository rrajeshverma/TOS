class StreakStatistics:
    """Calculates consecutive winning and losing trade streaks."""

    def max_consecutive_wins(
        self,
        trades: list,
    ) -> int:
        max_wins = 0
        current_wins = 0

        for trade in trades:
            if trade.pnl > 0:
                current_wins += 1
                max_wins = max(
                    max_wins,
                    current_wins,
                )
            else:
                current_wins = 0

        return max_wins

    def max_consecutive_losses(
        self,
        trades: list,
    ) -> int:
        max_losses = 0
        current_losses = 0

        for trade in trades:
            if trade.pnl < 0:
                current_losses += 1
                max_losses = max(
                    max_losses,
                    current_losses,
                )
            else:
                current_losses = 0

        return max_losses

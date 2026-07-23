class Statistics:
    """Statistical calculations for trading performance."""

    def win_rate(
        self,
        winning_trades: int,
        total_trades: int,
    ) -> float:
        if total_trades == 0:
            return 0.0

        return (winning_trades / total_trades) * 100.0

    def profit_factor(
        self,
        gross_profit: float,
        gross_loss: float,
    ) -> float:
        if gross_loss == 0:
            return 0.0

        return gross_profit / gross_loss

    def average_win(
        self,
        gross_profit: float,
        winning_trades: int,
    ) -> float:
        if winning_trades == 0:
            return 0.0

        return gross_profit / winning_trades

    def average_loss(
        self,
        gross_loss: float,
        losing_trades: int,
    ) -> float:
        if losing_trades == 0:
            return 0.0

        return gross_loss / losing_trades

    def expectancy(
        self,
        average_win: float,
        average_loss: float,
        win_rate: float,
    ) -> float:
        win_probability = win_rate / 100.0
        loss_probability = 1.0 - win_probability

        return (average_win * win_probability) - (average_loss * loss_probability)

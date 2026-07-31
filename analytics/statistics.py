import statistics


class Statistics:
    def win_rate(self, trades):
        if not trades:
            return 0.0

        wins = sum(1 for trade in trades if trade > 0)
        return (wins / len(trades)) * 100

    def average_win(self, trades):
        wins = [trade for trade in trades if trade > 0]

        if not wins:
            return 0.0

        return sum(wins) / len(wins)

    def average_loss(self, trades):
        losses = [-trade for trade in trades if trade < 0]

        if not losses:
            return 0.0

        return sum(losses) / len(losses)

    def profit_factor(self, trades):
        if not trades:
            return 0.0

        gross_profit = sum(trade for trade in trades if trade > 0)
        gross_loss = -sum(trade for trade in trades if trade < 0)

        if gross_loss == 0:
            return float("inf") if gross_profit > 0 else 0.0

        return gross_profit / gross_loss

    def payoff_ratio(self, trades):
        avg_win = self.average_win(trades)
        avg_loss = self.average_loss(trades)

        if avg_loss == 0:
            if avg_win > 0:
                return float("inf")
            return 0.0

        return avg_win / avg_loss

    def expectancy(self, trades):
        if not trades:
            return 0.0

        win_probability = self.win_rate(trades) / 100
        loss_probability = 1 - win_probability

        return win_probability * self.average_win(
            trades
        ) - loss_probability * self.average_loss(trades)

    def recovery_factor(self, net_profit, max_drawdown):
        if max_drawdown == 0:
            return float("inf") if net_profit > 0 else 0.0

        return net_profit / max_drawdown

    def sharpe_ratio(self, returns):
        if len(returns) < 2:
            return 0.0

        std_dev = statistics.stdev(returns)

        if std_dev == 0:
            return 0.0

        return statistics.mean(returns) / std_dev

    def sortino_ratio(self, returns):
        if len(returns) < 2:
            return 0.0

        downside_returns = [r for r in returns if r < 0]

        if len(downside_returns) < 2:
            return 0.0

        downside_std = statistics.stdev(downside_returns)

        if downside_std == 0:
            return 0.0

        return statistics.mean(returns) / downside_std

    def calmar_ratio(self, cagr, max_drawdown_percent):
        if max_drawdown_percent == 0:
            return float("inf") if cagr > 0 else 0.0

        return cagr / max_drawdown_percent

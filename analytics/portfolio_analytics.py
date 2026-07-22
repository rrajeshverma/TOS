from analytics.annual_return import AnnualReturn
from analytics.cagr import CAGR
from analytics.calmar_ratio import CalmarRatio
from analytics.expected_shortfall import ExpectedShortfall
from analytics.payoff_ratio import PayoffRatio
from analytics.recovery_ratio import RecoveryRatio
from analytics.sharpe_ratio import SharpeRatio
from analytics.sortino_ratio import SortinoRatio
from analytics.value_at_risk import ValueAtRisk
from analytics.volatility import Volatility


class PortfolioAnalytics:
    """Facade for portfolio analytics."""

    def __init__(self):
        self._sharpe = SharpeRatio()
        self._sortino = SortinoRatio()
        self._volatility = Volatility()
        self._calmar = CalmarRatio()
        self._cagr = CAGR()
        self._annual_return = AnnualReturn()
        self._payoff = PayoffRatio()
        self._recovery = RecoveryRatio()
        self._var = ValueAtRisk()
        self._expected_shortfall = ExpectedShortfall()

    def calculate(
        self,
        *,
        returns: list[float],
        beginning_value: float,
        ending_value: float,
        years: float,
        average_win: float,
        average_loss: float,
        net_profit: float,
        max_drawdown: float,
    ) -> dict[str, float]:

        annual_return = self._annual_return.calculate(
            beginning_value,
            ending_value,
        )

        return {
            "sharpe_ratio": self._sharpe.calculate(returns),
            "sortino_ratio": self._sortino.calculate(returns),
            "volatility": self._volatility.calculate(returns),
            "calmar_ratio": self._calmar.calculate(
                annual_return,
                max_drawdown,
            ),
            "cagr": self._cagr.calculate(
                beginning_value,
                ending_value,
                years,
            ),
            "annual_return": annual_return,
            "payoff_ratio": self._payoff.calculate(
                average_win,
                average_loss,
            ),
            "recovery_ratio": self._recovery.calculate(
                net_profit,
                max_drawdown,
            ),
            "value_at_risk": self._var.calculate(returns),
            "expected_shortfall": self._expected_shortfall.calculate(returns),
        }

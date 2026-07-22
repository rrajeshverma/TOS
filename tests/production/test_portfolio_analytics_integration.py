from analytics.annual_return import AnnualReturn
from analytics.cagr import CAGR
from analytics.calmar_ratio import CalmarRatio
from analytics.expected_shortfall import ExpectedShortfall
from analytics.payoff_ratio import PayoffRatio
from analytics.portfolio_analytics import PortfolioAnalytics
from analytics.recovery_ratio import RecoveryRatio
from analytics.sharpe_ratio import SharpeRatio
from analytics.sortino_ratio import SortinoRatio
from analytics.value_at_risk import ValueAtRisk
from analytics.volatility import Volatility


def build_metrics():
    returns = [0.02, -0.01, 0.03]

    return PortfolioAnalytics().calculate(
        returns=returns,
        beginning_value=100,
        ending_value=120,
        years=1,
        average_win=20,
        average_loss=10,
        net_profit=100,
        max_drawdown=20,
    )


def test_sharpe_matches():
    metrics = build_metrics()

    expected = SharpeRatio().calculate([0.02, -0.01, 0.03])

    assert metrics["sharpe_ratio"] == expected


def test_sortino_matches():
    metrics = build_metrics()

    expected = SortinoRatio().calculate([0.02, -0.01, 0.03])

    assert metrics["sortino_ratio"] == expected


def test_volatility_matches():
    metrics = build_metrics()

    expected = Volatility().calculate([0.02, -0.01, 0.03])

    assert metrics["volatility"] == expected


def test_cagr_matches():
    metrics = build_metrics()

    expected = CAGR().calculate(
        100,
        120,
        1,
    )

    assert metrics["cagr"] == expected


def test_annual_return_matches():
    metrics = build_metrics()

    expected = AnnualReturn().calculate(
        100,
        120,
    )

    assert metrics["annual_return"] == expected


def test_calmar_matches():
    metrics = build_metrics()

    annual = AnnualReturn().calculate(
        100,
        120,
    )

    expected = CalmarRatio().calculate(
        annual,
        20,
    )

    assert metrics["calmar_ratio"] == expected


def test_payoff_matches():
    metrics = build_metrics()

    expected = PayoffRatio().calculate(
        20,
        10,
    )

    assert metrics["payoff_ratio"] == expected


def test_recovery_matches():
    metrics = build_metrics()

    expected = RecoveryRatio().calculate(
        100,
        20,
    )

    assert metrics["recovery_ratio"] == expected


def test_var_matches():
    metrics = build_metrics()

    expected = ValueAtRisk().calculate([0.02, -0.01, 0.03])

    assert metrics["value_at_risk"] == expected


def test_expected_shortfall_matches():
    metrics = build_metrics()

    expected = ExpectedShortfall().calculate([0.02, -0.01, 0.03])

    assert metrics["expected_shortfall"] == expected

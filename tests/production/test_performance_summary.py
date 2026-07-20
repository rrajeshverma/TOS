from reporting.models.performance_summary import (
    PerformanceSummary,
)


def test_create_summary():
    summary = PerformanceSummary()

    assert summary.trade_metrics is None
    assert summary.portfolio_metrics == {}


def test_assign_trade_metrics():
    summary = PerformanceSummary()

    summary.trade_metrics = object()

    assert summary.trade_metrics is not None


def test_assign_portfolio_metrics():
    summary = PerformanceSummary()

    summary.portfolio_metrics = {
        "sharpe_ratio": 1.5,
    }

    assert summary.portfolio_metrics[
        "sharpe_ratio"
    ] == 1.5


def test_summary_contains_dictionary():
    summary = PerformanceSummary()

    summary.portfolio_metrics = {
        "a": 1.0
    }

    assert isinstance(
        summary.portfolio_metrics,
        dict,
    )


def test_summary_defaults():
    summary = PerformanceSummary()

    assert summary.portfolio_metrics == {}
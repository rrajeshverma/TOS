from analytics.performance_report import PerformanceReport


def test_generate_report():
    report = PerformanceReport()

    trades = [100, -50, 300, -150]

    result = report.generate(
        initial_capital=100000,
        ending_capital=100200,
        years=1,
        trades=trades,
    )

    assert result["initial_capital"] == 100000
    assert result["ending_capital"] == 100200
    assert result["total_trades"] == 4
    assert result["win_rate"] == 50.0

def test_generate_performance_report_with_advanced_metrics():
    report = PerformanceReport()

    result = report.generate(
        initial_capital=100000,
        ending_capital=110000,
        years=1,
        trades=[100, -50, 200, -100],
        max_drawdown_percent=10.0,
        returns_series=[0.01, 0.02, -0.01, 0.03],
    )

    assert "recovery_factor" in result
    assert "sharpe_ratio" in result
    assert "sortino_ratio" in result
    assert "calmar_ratio" in result
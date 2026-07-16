from reporting.reports.performance_report import PerformanceReport
from reporting.reports.report_generator import ReportGenerator
from reporting.models.performance_model import PerformanceModel


from reporting.models.performance_model import PerformanceModel

def test_generate_report():
    generator = ReportGenerator()

    performance = PerformanceModel()

    report = generator.generate(performance)

    assert isinstance(report, PerformanceReport)

def test_generate_report_from_performance():
    generator = ReportGenerator()

    performance = PerformanceModel()
    performance.total_trades = 25
    performance.net_profit = 5000.0

    report = generator.generate(performance)

    assert report.performance.total_trades == 25
    assert report.performance.net_profit == 5000.0

def test_report_contains_summary():
    generator = ReportGenerator()

    performance = PerformanceModel()
    performance.total_trades = 10
    performance.net_profit = 2500.0

    report = generator.generate(performance)

    assert "Total Trades: 10" in report.summary
    assert "Net Profit: 2500.0" in report.summary

def test_report_contains_trade_section():
    generator = ReportGenerator()

    performance = PerformanceModel()
    performance.total_trades = 15
    performance.winning_trades = 9
    performance.losing_trades = 6

    report = generator.generate(performance)

    assert "Trades" in report.summary
    assert "Total Trades: 15" in report.summary
    assert "Winning Trades: 9" in report.summary
    assert "Losing Trades: 6" in report.summary

def test_report_contains_profit_section():
    generator = ReportGenerator()

    performance = PerformanceModel()
    performance.gross_profit = 6500.0
    performance.gross_loss = 2400.0
    performance.net_profit = 4100.0

    report = generator.generate(performance)

    assert "Profit" in report.summary
    assert "Gross Profit: 6500.0" in report.summary
    assert "Gross Loss: 2400.0" in report.summary
    assert "Net Profit: 4100.0" in report.summary

def test_report_contains_performance_section():
    generator = ReportGenerator()

    performance = PerformanceModel()
    performance.win_rate = 64.0
    performance.profit_factor = 2.71
    performance.expectancy = 165.5
    performance.recovery_factor = 1.85

    report = generator.generate(performance)

    assert "Performance" in report.summary
    assert "Win Rate: 64.0" in report.summary
    assert "Profit Factor: 2.71" in report.summary
    assert "Expectancy: 165.5" in report.summary
    assert "Recovery Factor: 1.85" in report.summary

def test_report_contains_risk_section():
    generator = ReportGenerator()

    performance = PerformanceModel()
    performance.peak_equity = 5200.0
    performance.max_drawdown = 950.0
    performance.max_drawdown_percent = 18.27

    report = generator.generate(performance)

    assert "Risk" in report.summary
    assert "Peak Equity: 5200.0" in report.summary
    assert "Maximum Drawdown: 950.0" in report.summary
    assert "Maximum Drawdown %: 18.27" in report.summary

def test_report_contains_streaks_section():
    generator = ReportGenerator()

    performance = PerformanceModel()
    performance.max_consecutive_wins = 5
    performance.max_consecutive_losses = 2

    report = generator.generate(performance)

    assert "Streaks" in report.summary
    assert "Maximum Consecutive Wins: 5" in report.summary
    assert "Maximum Consecutive Losses: 2" in report.summary
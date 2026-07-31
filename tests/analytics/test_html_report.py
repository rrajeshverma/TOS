from analytics.html_report import HTMLReport


def test_generate_empty_report():
    report = HTMLReport()

    html = report.generate(
        summary={
            "initial_capital": 100000,
            "final_capital": 100000,
            "net_profit": 0,
            "win_rate": 0,
        }
    )

    assert "<html>" in html
    assert "Initial Capital" in html
    assert "100000" in html


def test_generate_profit_report():
    report = HTMLReport()

    html = report.generate(
        summary={
            "initial_capital": 100000,
            "final_capital": 100225,
            "net_profit": 225,
            "win_rate": 50.0,
        }
    )

    assert "100225" in html
    assert "225" in html
    assert "50.0" in html

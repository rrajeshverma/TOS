"""
Integration Test:

Daily Trading Report Flow

Validates:
- Trade aggregation
- P&L calculation
- Win/Loss statistics
- Report generation
"""


from decimal import Decimal


class DailyTradingReport:

    def __init__(
        self,
        trades,
    ) -> None:

        self.trades = trades


    def total_trades(self):

        return len(
            self.trades
        )


    def winning_trades(self):

        return len(
            [
                trade
                for trade in self.trades
                if trade["pnl"] > 0
            ]
        )


    def losing_trades(self):

        return len(
            [
                trade
                for trade in self.trades
                if trade["pnl"] < 0
            ]
        )


    def gross_pnl(self):

        return sum(
            trade["pnl"]
            for trade in self.trades
        )


    def generate(self):

        total = self.total_trades()

        wins = self.winning_trades()

        return {
            "total_trades": total,
            "winning_trades": wins,
            "losing_trades": self.losing_trades(),
            "gross_pnl": self.gross_pnl(),
            "win_rate": (
                Decimal(wins)
                / Decimal(total)
                * Decimal("100")
                if total
                else Decimal("0")
            ),
        }


def create_trades():

    return [
        {
            "symbol": "NIFTY",
            "pnl": Decimal("1500"),
        },
        {
            "symbol": "NIFTY",
            "pnl": Decimal("-500"),
        },
        {
            "symbol": "NIFTY",
            "pnl": Decimal("1000"),
        },
    ]


def test_report_counts_total_trades():

    report = DailyTradingReport(
        create_trades()
    )

    assert (
        report.total_trades()
        == 3
    )


def test_report_counts_winning_trades():

    report = DailyTradingReport(
        create_trades()
    )

    assert (
        report.winning_trades()
        == 2
    )


def test_report_counts_losing_trades():

    report = DailyTradingReport(
        create_trades()
    )

    assert (
        report.losing_trades()
        == 1
    )


def test_report_calculates_gross_pnl():

    report = DailyTradingReport(
        create_trades()
    )

    assert (
        report.gross_pnl()
        == Decimal("2000")
    )


def test_daily_report_generation():

    report = DailyTradingReport(
        create_trades()
    )

    summary = report.generate()

    assert (
        summary["total_trades"]
        == 3
    )

    assert (
        summary["gross_pnl"]
        == Decimal("2000")
    )

    assert (
        summary["win_rate"]
        == Decimal("66.66666666666666666666666667")
    )

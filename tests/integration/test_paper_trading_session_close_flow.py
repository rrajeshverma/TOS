"""
Integration Test:

Paper Trading Session Close Flow

Validates safe end-of-day processing.
"""

from decimal import Decimal


class PaperTradingSession:
    def __init__(self):
        self.running = True
        self.orders_enabled = True
        self.closed = False

    def stop_orders(self):
        self.orders_enabled = False

    def calculate_pnl(
        self,
        trades,
    ):
        return sum(trade["pnl"] for trade in trades)

    def close(self):
        self.stop_orders()

        self.running = False

        self.closed = True


class DailyReport:
    def __init__(self):
        self.generated = False
        self.data = None

    def generate(
        self,
        pnl,
    ):
        self.data = {
            "net_pnl": pnl,
            "status": "CLOSED",
        }

        self.generated = True


class JournalBackup:
    def __init__(self):
        self.saved = False

    def save(self):
        self.saved = True


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
    ]


def test_session_stops_new_orders():
    session = PaperTradingSession()

    session.stop_orders()

    assert session.orders_enabled is False


def test_session_calculates_daily_pnl():
    session = PaperTradingSession()

    pnl = session.calculate_pnl(create_trades())

    assert pnl == Decimal("1000")


def test_daily_report_generation():
    report = DailyReport()

    report.generate(Decimal("1000"))

    assert report.generated is True

    assert report.data["status"] == "CLOSED"


def test_journal_backup():
    backup = JournalBackup()

    backup.save()

    assert backup.saved is True


def test_complete_session_close_flow():
    session = PaperTradingSession()

    report = DailyReport()

    backup = JournalBackup()

    session.stop_orders()

    pnl = session.calculate_pnl(create_trades())

    report.generate(pnl)

    session.close()

    backup.save()

    assert session.running is False

    assert session.closed is True

    assert report.data["net_pnl"] == Decimal("1000")

    assert backup.saved is True

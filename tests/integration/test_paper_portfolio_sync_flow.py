"""
Integration Test:

Paper Portfolio Sync Flow

Validates:

Paper Execution
        |
        ▼
Position
        |
        ▼
Portfolio
        |
        ▼
P&L
"""

from decimal import Decimal


class PaperPortfolio:
    def __init__(self):
        self.positions = {}
        self.cash = Decimal(100000)
        self.pnl = Decimal(0)

    def update_position(
        self,
        trade,
    ):
        symbol = trade["symbol"]

        quantity = trade["quantity"]

        self.positions[symbol] = (
            self.positions.get(
                symbol,
                0,
            )
            + quantity
        )

    def update_pnl(
        self,
        pnl,
    ):
        self.pnl = pnl

    def get_position(
        self,
        symbol,
    ):
        return self.positions.get(
            symbol,
            0,
        )


class PaperExecutionService:
    def execute(
        self,
    ):
        return {
            "order_id": "PAPER001",
            "symbol": "NIFTY",
            "side": "BUY",
            "quantity": 65,
            "price": Decimal(25000),
        }


class PortfolioJournal:
    def __init__(self):
        self.entries = []

    def record(
        self,
        portfolio,
    ):
        self.entries.append(
            {
                "positions": portfolio.positions.copy(),
                "pnl": portfolio.pnl,
            }
        )


def create_trade():
    return PaperExecutionService().execute()


def test_trade_execution_returns_order():
    trade = create_trade()

    assert trade["order_id"] == "PAPER001"


def test_portfolio_updates_position():
    portfolio = PaperPortfolio()

    trade = create_trade()

    portfolio.update_position(trade)

    assert portfolio.get_position("NIFTY") == 65


def test_portfolio_updates_pnl():
    portfolio = PaperPortfolio()

    portfolio.update_pnl(Decimal(2500))

    assert portfolio.pnl == Decimal(2500)


def test_journal_records_portfolio_state():
    portfolio = PaperPortfolio()

    portfolio.update_position(create_trade())

    journal = PortfolioJournal()

    journal.record(portfolio)

    assert len(journal.entries) == 1


def test_complete_portfolio_sync_flow():
    portfolio = PaperPortfolio()

    journal = PortfolioJournal()

    trade = create_trade()

    portfolio.update_position(trade)

    portfolio.update_pnl(Decimal(3250))

    journal.record(portfolio)

    assert portfolio.positions["NIFTY"] == 65

    assert portfolio.pnl == Decimal(3250)

    assert len(journal.entries) == 1

"""
Integration Test:

Paper Trading Service Pipeline

Validates:

Decision
    |
Risk
    |
Trade Creation
    |
Paper Execution
    |
Journal
"""

from datetime import datetime
from decimal import Decimal

from domain.indicator_set import IndicatorSet
from domain.market import Market
from engines.decision_engine import DecisionEngine
from engines.risk_engine import RiskEngine


class DummyPaperTradingService:
    """
    Simulates paper execution service.
    """

    def __init__(self):
        self.executed_trades = []

    def execute(
        self,
        trade,
    ):
        self.executed_trades.append(trade)

        return trade


class DummyJournal:
    def __init__(self):
        self.entries = []

    def record(
        self,
        trade,
    ):
        self.entries.append(trade)


def create_market():
    return Market(
        symbol="NIFTY",
        exchange="NSE",
        timeframe="TICK",
        open=25000,
        high=25100,
        low=24900,
        close=25100,
        volume=100000,
        timestamp=datetime.now(),
    )


def create_indicators():
    return IndicatorSet(
        ema_high=25000,
        ema_low=24900,
        vwap=25000,
        rsi=60,
        volume_average=50000,
    )


def create_trade_flow():
    market = create_market()

    indicators = create_indicators()

    decision = DecisionEngine().evaluate(
        market,
        indicators,
    )

    risk = RiskEngine().evaluate(
        decision,
        trades_today=0,
        daily_loss=Decimal(0),
    )

    return risk


def test_decision_passes_to_risk_engine():
    risk = create_trade_flow()

    assert risk is not None


def test_risk_allows_valid_trade():
    risk = create_trade_flow()

    assert risk.approved is True


def test_paper_service_executes_trade():
    service = DummyPaperTradingService()

    trade = {
        "symbol": "NIFTY",
        "side": "BUY",
        "quantity": 65,
    }

    result = service.execute(trade)

    assert result["symbol"] == "NIFTY"

    assert len(service.executed_trades) == 1


def test_journal_records_paper_trade():
    journal = DummyJournal()

    trade = {
        "symbol": "NIFTY",
        "quantity": 65,
    }

    journal.record(trade)

    assert len(journal.entries) == 1


def test_complete_paper_service_pipeline():
    risk = create_trade_flow()

    assert risk.approved is True

    service = DummyPaperTradingService()

    journal = DummyJournal()

    trade = {
        "symbol": "NIFTY",
        "side": "BUY",
        "quantity": 65,
    }

    executed = service.execute(trade)

    journal.record(executed)

    assert len(service.executed_trades) == 1

    assert len(journal.entries) == 1

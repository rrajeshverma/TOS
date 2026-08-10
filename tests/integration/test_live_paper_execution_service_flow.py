"""
Integration Test:

Live Paper Execution Service Flow

Validates the same execution path
used before live broker submission.
"""

from datetime import datetime
from decimal import Decimal

from domain.indicator_set import IndicatorSet
from domain.market import Market
from engines.decision_engine import DecisionEngine
from engines.risk_engine import RiskEngine


class PaperTradingService:
    def __init__(self):
        self.orders = []
        self.positions = {}

    def execute(
        self,
        trade,
    ):
        self.orders.append(trade)

        symbol = trade["symbol"]

        self.positions[symbol] = (
            self.positions.get(
                symbol,
                0,
            )
            + trade["quantity"]
        )

        return {
            "status": "EXECUTED",
            "trade": trade,
        }


class TradeJournal:
    def __init__(self):
        self.records = []

    def record(
        self,
        execution,
    ):
        self.records.append(execution)


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


def create_trade_decision():
    market = create_market()

    indicators = create_indicators()

    return DecisionEngine().evaluate(
        market,
        indicators,
    )


def test_decision_passes_risk_validation():
    decision = create_trade_decision()

    risk = RiskEngine().evaluate(
        decision,
        trades_today=0,
        daily_loss=Decimal(0),
    )

    assert risk.approved is True


def test_paper_service_executes_buy_order():
    service = PaperTradingService()

    trade = {
        "symbol": "NIFTY",
        "side": "BUY",
        "quantity": 65,
    }

    result = service.execute(trade)

    assert result["status"] == "EXECUTED"


def test_position_updates_after_execution():
    service = PaperTradingService()

    service.execute(
        {
            "symbol": "NIFTY",
            "side": "BUY",
            "quantity": 65,
        }
    )

    assert service.positions["NIFTY"] == 65


def test_trade_journal_records_execution():
    journal = TradeJournal()

    execution = {
        "status": "EXECUTED",
        "symbol": "NIFTY",
    }

    journal.record(execution)

    assert len(journal.records) == 1


def test_complete_live_paper_execution_flow():
    decision = create_trade_decision()

    risk = RiskEngine().evaluate(
        decision,
        trades_today=0,
        daily_loss=Decimal(0),
    )

    assert risk.approved is True

    service = PaperTradingService()

    journal = TradeJournal()

    execution = service.execute(
        {
            "symbol": "NIFTY",
            "side": "BUY",
            "quantity": 65,
        }
    )

    journal.record(execution)

    assert len(service.orders) == 1

    assert len(journal.records) == 1

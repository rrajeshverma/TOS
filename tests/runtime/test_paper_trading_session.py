"""
Unit Tests:

Paper Trading Session Runtime
"""

import pytest

from runtime.paper_trading_session import (
    PaperTradingSession,
)


class DummyStrategy:
    def evaluate(
        self,
        tick,
    ):
        return {
            "symbol": tick["symbol"],
            "side": "BUY",
            "quantity": 65,
        }


class DummyExecutor:
    def execute(
        self,
        decision,
    ):
        return {
            "trade_id": "PAPER001",
            "symbol": decision["symbol"],
            "quantity": decision["quantity"],
        }


class DummyJournal:
    def __init__(self):
        self.records = []

    def record(
        self,
        trade,
    ):
        self.records.append(trade)


def create_session():
    return PaperTradingSession(
        strategy=DummyStrategy(),
        executor=DummyExecutor(),
        journal=DummyJournal(),
    )


def create_tick():
    return {
        "symbol": "NIFTY",
        "price": 25000,
    }


def test_session_starts():
    session = create_session()

    session.start()

    assert session.is_running() is True


def test_session_stops():
    session = create_session()

    session.start()

    session.stop()

    assert session.is_running() is False


def test_tick_before_start_is_rejected():
    session = create_session()

    with pytest.raises(RuntimeError):
        session.process_tick(create_tick())


def test_tick_creates_paper_trade():
    session = create_session()

    session.start()

    trade = session.process_tick(create_tick())

    assert trade is not None

    assert trade["symbol"] == "NIFTY"


def test_trade_is_recorded_in_journal():
    session = create_session()

    session.start()

    session.process_tick(create_tick())

    assert len(session.journal.records) == 1


def test_session_summary():
    session = create_session()

    session.start()

    session.process_tick(create_tick())

    summary = session.summary()

    assert summary["running"] is True

    assert summary["trades"] == 1


def test_process_tick_without_strategy_returns_none():
    session = PaperTradingSession()

    session.start()

    assert session.process_tick(create_tick()) is None


class NoSignalStrategy:
    def evaluate(
        self,
        tick,
    ):
        return None


def test_process_tick_without_signal_returns_none():
    session = PaperTradingSession(
        strategy=NoSignalStrategy(),
        executor=DummyExecutor(),
        journal=DummyJournal(),
    )

    session.start()

    assert session.process_tick(create_tick()) is None


def test_process_tick_without_executor_returns_none():
    session = PaperTradingSession(
        strategy=DummyStrategy(),
        executor=None,
        journal=DummyJournal(),
    )

    session.start()

    assert session.process_tick(create_tick()) is None


class NullExecutor:
    def execute(
        self,
        decision,
    ):
        return None


def test_executor_returning_none_creates_no_trade():
    session = PaperTradingSession(
        strategy=DummyStrategy(),
        executor=NullExecutor(),
        journal=DummyJournal(),
    )

    session.start()

    trade = session.process_tick(create_tick())

    assert trade is None
    assert session.trades == []
    assert session.journal.records == []


def test_summary_before_start():
    session = create_session()

    summary = session.summary()

    assert summary["running"] is False
    assert summary["trades"] == 0
    assert "timestamp" in summary

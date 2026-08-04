"""
Tests for TradeRecorder.
"""

from __future__ import annotations

from unittest.mock import Mock

from backtesting.trade_recorder import TradeRecorder


def test_record_trade():
    recorder = TradeRecorder()

    trade = Mock()

    recorder.record(trade)

    assert recorder.total_trades == 1
    assert recorder.trades == [trade]


def test_clear_trades():
    recorder = TradeRecorder()

    recorder.record(Mock())
    recorder.record(Mock())

    assert recorder.total_trades == 2

    recorder.clear()

    assert recorder.total_trades == 0
    assert recorder.trades == []

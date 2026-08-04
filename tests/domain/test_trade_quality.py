"""
Tests for TradeQuality domain object.
"""

from domain.trade_quality import TradeQuality


def test_trade_quality_approved():
    quality = TradeQuality(
        approved=True,
        reasons=(),
    )

    assert quality.is_approved
    assert quality.reason_count == 0


def test_trade_quality_rejected():
    quality = TradeQuality(
        approved=False,
        reasons=(
            "Big candle",
            "ATR too high",
        ),
    )

    assert not quality.is_approved
    assert quality.reason_count == 2

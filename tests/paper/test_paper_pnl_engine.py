import pytest

from paper.paper_pnl_engine import PaperPnLEngine


def test_can_create_engine():
    assert PaperPnLEngine() is not None


def test_zero_pnl_initial():
    engine = PaperPnLEngine()

    assert engine.realized_pnl == 0


def test_zero_unrealized_initial():
    engine = PaperPnLEngine()

    assert engine.unrealized_pnl == 0


def test_buy_position_has_zero_realized():
    engine = PaperPnLEngine()

    engine.buy("NIFTY", 10, 100)

    assert engine.realized_pnl == 0


def test_sell_after_buy_generates_profit():
    engine = PaperPnLEngine()

    engine.buy("NIFTY", 10, 100)
    engine.sell("NIFTY", 10, 110)

    assert engine.realized_pnl == 100


def test_sell_after_buy_generates_loss():
    engine = PaperPnLEngine()

    engine.buy("NIFTY", 10, 100)
    engine.sell("NIFTY", 10, 90)

    assert engine.realized_pnl == -100


def test_mark_to_market_profit():
    engine = PaperPnLEngine()

    engine.buy("NIFTY", 10, 100)

    assert engine.mark_to_market("NIFTY", 110) == 100


def test_mark_to_market_loss():
    engine = PaperPnLEngine()

    engine.buy("NIFTY", 10, 100)

    assert engine.mark_to_market("NIFTY", 90) == -100


def test_unknown_symbol_returns_zero():
    engine = PaperPnLEngine()

    assert engine.mark_to_market("ABC", 100) == 0


def test_multiple_symbols():
    engine = PaperPnLEngine()

    engine.buy("NIFTY", 10, 100)
    engine.buy("BANKNIFTY", 5, 200)

    assert len(engine.positions()) == 2


def test_reject_negative_quantity():
    engine = PaperPnLEngine()

    with pytest.raises(ValueError):
        engine.buy("NIFTY", -1, 100)


def test_reject_zero_price():
    engine = PaperPnLEngine()

    with pytest.raises(ValueError):
        engine.buy("NIFTY", 1, 0)


def test_repeatable_queries():
    engine = PaperPnLEngine()

    assert engine.positions() == engine.positions()


def test_position_count():
    engine = PaperPnLEngine()

    engine.buy("NIFTY", 1, 100)

    assert len(engine.positions()) == 1


def test_empty_positions():
    engine = PaperPnLEngine()

    assert engine.positions() == {}


def test_sell_invalid_quantity():
    engine = PaperPnLEngine()

    with pytest.raises(ValueError, match="quantity must be positive"):
        engine.sell("NIFTY", 0, 100)


def test_sell_invalid_price():
    engine = PaperPnLEngine()

    with pytest.raises(ValueError, match="price must be positive"):
        engine.sell("NIFTY", 1, 0)


def test_sell_unknown_symbol_keeps_realized_pnl_zero():
    engine = PaperPnLEngine()

    engine.sell("UNKNOWN", 10, 100)

    assert engine.realized_pnl == 0


def test_buy_overwrites_existing_position():
    engine = PaperPnLEngine()

    engine.buy("NIFTY", 10, 100)
    engine.buy("NIFTY", 20, 200)

    position = engine.positions()["NIFTY"]

    assert position["quantity"] == 20
    assert position["price"] == 200


def test_positions_returns_current_positions():
    engine = PaperPnLEngine()

    engine.buy("NIFTY", 5, 100)

    positions = engine.positions()

    assert "NIFTY" in positions
    assert positions["NIFTY"]["quantity"] == 5

import pytest

from paper.paper_order_service import PaperOrderService
from paper.paper_position_book import PaperPositionBook
from paper.paper_portfolio import PaperPortfolio
from paper.paper_trading_pipeline import PaperTradingPipeline


def trade(symbol="NIFTY", side="BUY", quantity=50, price=25000.0):
    return {
        "symbol": symbol,
        "side": side,
        "quantity": quantity,
        "price": price,
    }


def pipeline():
    return PaperTradingPipeline(
        PaperOrderService(),
        PaperPositionBook(),
        PaperPortfolio(),
    )


def test_can_create_pipeline():
    assert pipeline() is not None


def test_buy_creates_order():
    p = pipeline()

    result = p.execute(trade())

    assert result.startswith("PAPER-")


def test_buy_creates_position():
    p = pipeline()

    p.execute(trade())

    assert p.position_book.get("NIFTY")["quantity"] == 50


def test_buy_updates_portfolio():
    p = pipeline()

    p.execute(trade())

    assert p.portfolio.position("NIFTY") == 50


def test_sell_reduces_position():
    p = pipeline()

    p.execute(trade())
    p.execute(trade(side="SELL"))

    assert p.position_book.get("NIFTY")["quantity"] == 0


def test_sell_updates_portfolio():
    p = pipeline()

    p.execute(trade())
    p.execute(trade(side="SELL"))

    assert p.portfolio.position("NIFTY") == 0


def test_multiple_symbols():
    p = pipeline()

    p.execute(trade("NIFTY"))
    p.execute(trade("BANKNIFTY"))

    assert len(p.position_book.positions()) == 2


def test_invalid_trade():
    p = pipeline()

    with pytest.raises(ValueError):
        p.execute(None)


def test_repeatable():
    p = pipeline()

    assert p.execute(trade()).startswith("PAPER-")


def test_unique_order_ids():
    p = pipeline()

    first = p.execute(trade())
    second = p.execute(trade())

    assert first != second


def test_order_count():
    p = pipeline()

    p.execute(trade())
    p.execute(trade())

    assert len(p.order_service.orders) == 2


def test_position_book_shared():
    p = pipeline()

    p.execute(trade())

    assert p.position_book.get("NIFTY") is not None


def test_portfolio_shared():
    p = pipeline()

    p.execute(trade())

    assert len(p.portfolio.positions()) == 1


def test_pipeline_keeps_dependencies():
    p = pipeline()

    assert p.order_service is not None
    assert p.position_book is not None
    assert p.portfolio is not None


def test_multiple_buys_accumulate():
    p = pipeline()

    p.execute(trade(quantity=25))
    p.execute(trade(quantity=25))

    assert p.portfolio.position("NIFTY") == 50

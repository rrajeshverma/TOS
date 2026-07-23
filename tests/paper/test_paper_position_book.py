import pytest

from paper.paper_position_book import PaperPositionBook


def buy(symbol="NIFTY", quantity=50, price=25000.0):
    return {
        "symbol": symbol,
        "side": "BUY",
        "quantity": quantity,
        "price": price,
    }


def sell(symbol="NIFTY", quantity=50, price=25000.0):
    return {
        "symbol": symbol,
        "side": "SELL",
        "quantity": quantity,
        "price": price,
    }


def test_can_create_position_book():
    assert PaperPositionBook() is not None


def test_create_long_position():
    book = PaperPositionBook()

    book.record(buy())

    position = book.get("NIFTY")

    assert position["quantity"] == 50


def test_create_short_position():
    book = PaperPositionBook()

    book.record(sell())

    position = book.get("NIFTY")

    assert position["quantity"] == -50


def test_rejects_none_trade():
    book = PaperPositionBook()

    with pytest.raises(ValueError):
        book.record(None)


def test_preserves_symbol():
    book = PaperPositionBook()

    book.record(buy())

    assert book.get("NIFTY")["symbol"] == "NIFTY"


def test_preserves_price():
    book = PaperPositionBook()

    book.record(buy(price=25100.0))

    assert book.get("NIFTY")["price"] == 25100.0


def test_adds_to_existing_position():
    book = PaperPositionBook()

    book.record(buy(quantity=50))
    book.record(buy(quantity=25))

    assert book.get("NIFTY")["quantity"] == 75


def test_reduces_existing_position():
    book = PaperPositionBook()

    book.record(buy(quantity=100))
    book.record(sell(quantity=40))

    assert book.get("NIFTY")["quantity"] == 60


def test_closes_position():
    book = PaperPositionBook()

    book.record(buy(quantity=50))
    book.record(sell(quantity=50))

    assert book.get("NIFTY")["quantity"] == 0


def test_lists_positions():
    book = PaperPositionBook()

    book.record(buy("NIFTY"))
    book.record(buy("BANKNIFTY"))

    assert len(book.positions()) == 2


def test_unknown_symbol_returns_none():
    book = PaperPositionBook()

    assert book.get("UNKNOWN") is None


def test_multiple_symbols():
    book = PaperPositionBook()

    book.record(buy("NIFTY"))
    book.record(buy("BANKNIFTY"))

    assert book.get("BANKNIFTY")["symbol"] == "BANKNIFTY"


def test_repeatable_reads():
    book = PaperPositionBook()

    book.record(buy())

    assert book.get("NIFTY") == book.get("NIFTY")


def test_position_count():
    book = PaperPositionBook()

    book.record(buy("NIFTY"))
    book.record(buy("BANKNIFTY"))

    assert len(book.positions()) == 2


def test_empty_book():
    book = PaperPositionBook()

    assert book.positions() == []

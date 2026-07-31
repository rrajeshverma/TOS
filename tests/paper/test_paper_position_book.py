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


# ---------------------------------------------------------
# Additional Certification Tests
# ---------------------------------------------------------


def test_latest_price_replaces_previous_price():
    book = PaperPositionBook()

    book.record(buy(price=25000.0))
    book.record(buy(price=25125.0))

    assert book.get("NIFTY")["price"] == 25125.0


def test_sell_updates_latest_price():
    book = PaperPositionBook()

    book.record(buy(price=25000.0))
    book.record(sell(quantity=10, price=24950.0))

    assert book.get("NIFTY")["price"] == 24950.0


def test_multiple_sells_create_short_position():
    book = PaperPositionBook()

    book.record(sell(quantity=25))
    book.record(sell(quantity=25))

    assert book.get("NIFTY")["quantity"] == -50


def test_buy_after_short_reduces_short_position():
    book = PaperPositionBook()

    book.record(sell(quantity=100))
    book.record(buy(quantity=40))

    assert book.get("NIFTY")["quantity"] == -60


def test_positions_returns_list():
    book = PaperPositionBook()

    assert isinstance(book.positions(), list)


def test_positions_returns_same_object_reference():
    book = PaperPositionBook()

    book.record(buy())

    position = book.get("NIFTY")

    assert position in book.positions()


def test_record_zero_quantity():
    book = PaperPositionBook()

    book.record(buy(quantity=0))

    assert book.get("NIFTY")["quantity"] == 0


def test_multiple_reads_after_updates():
    book = PaperPositionBook()

    book.record(buy(quantity=50))
    book.record(buy(quantity=10))

    first = book.get("NIFTY")
    second = book.get("NIFTY")

    assert first == second


def test_independent_symbol_updates():
    book = PaperPositionBook()

    book.record(buy("NIFTY", quantity=50))
    book.record(buy("BANKNIFTY", quantity=20))
    book.record(sell("NIFTY", quantity=10))

    assert book.get("NIFTY")["quantity"] == 40
    assert book.get("BANKNIFTY")["quantity"] == 20


def test_positions_contains_all_symbols():
    book = PaperPositionBook()

    book.record(buy("NIFTY"))
    book.record(buy("BANKNIFTY"))
    book.record(buy("FINNIFTY"))

    symbols = {p["symbol"] for p in book.positions()}

    assert symbols == {"NIFTY", "BANKNIFTY", "FINNIFTY"}

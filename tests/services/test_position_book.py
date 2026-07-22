from services.position_book import PositionBook


def test_position_book_starts_empty():

    book = PositionBook()

    assert book.count() == 0


def test_add_position():

    book = PositionBook()

    position = object()

    book.add_position(
        "P001",
        position,
    )

    assert book.count() == 1


def test_get_position():

    book = PositionBook()

    position = object()

    book.add_position(
        "P001",
        position,
    )

    assert book.get_position("P001") == position


def test_contains_position():

    book = PositionBook()

    book.add_position(
        "P001",
        object(),
    )

    assert book.contains("P001")


def test_remove_position():

    book = PositionBook()

    book.add_position(
        "P001",
        object(),
    )

    book.remove_position("P001")

    assert book.count() == 0


def test_clear_positions():

    book = PositionBook()

    book.add_position(
        "P001",
        object(),
    )

    book.clear()

    assert book.count() == 0


def test_remove_unknown_position():

    book = PositionBook()

    book.remove_position(
        "UNKNOWN"
    )

    assert book.count() == 0
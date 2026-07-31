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

    book.remove_position("UNKNOWN")

    assert book.count() == 0


# ---------------------------------------------------------
# Additional Certification Tests
# ---------------------------------------------------------


def test_get_unknown_position_returns_none():
    book = PositionBook()

    assert book.get_position("UNKNOWN") is None


def test_get_all_positions_empty():
    book = PositionBook()

    assert book.get_all_positions() == []


def test_get_all_positions_returns_all():
    book = PositionBook()

    p1 = object()
    p2 = object()

    book.add_position("P001", p1)
    book.add_position("P002", p2)

    positions = book.get_all_positions()

    assert len(positions) == 2
    assert p1 in positions
    assert p2 in positions


def test_contains_unknown_position():
    book = PositionBook()

    assert not book.contains("UNKNOWN")


def test_add_same_position_id_overwrites():
    book = PositionBook()

    first = object()
    second = object()

    book.add_position("P001", first)
    book.add_position("P001", second)

    assert book.count() == 1
    assert book.get_position("P001") is second


def test_clear_empty_book():
    book = PositionBook()

    book.clear()

    assert book.count() == 0


def test_count_after_multiple_additions():
    book = PositionBook()

    book.add_position("P001", object())
    book.add_position("P002", object())
    book.add_position("P003", object())

    assert book.count() == 3


def test_remove_one_preserves_others():
    book = PositionBook()

    p1 = object()
    p2 = object()

    book.add_position("P001", p1)
    book.add_position("P002", p2)

    book.remove_position("P001")

    assert not book.contains("P001")
    assert book.contains("P002")
    assert book.count() == 1


def test_get_all_positions_returns_list():
    book = PositionBook()

    assert isinstance(book.get_all_positions(), list)


def test_clear_removes_all_positions():
    book = PositionBook()

    book.add_position("P001", object())
    book.add_position("P002", object())

    book.clear()

    assert book.get_all_positions() == []
    assert book.count() == 0

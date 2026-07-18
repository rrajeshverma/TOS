from portfolio.strategy_context import StrategyContext


def test_create_context():
    context = StrategyContext()

    assert context is not None


def test_set_get():
    context = StrategyContext()

    context.set(
        "price",
        100,
    )

    assert context.get(
        "price"
    ) == 100


def test_get_default():
    context = StrategyContext()

    assert context.get(
        "missing",
        10,
    ) == 10


def test_contains():
    context = StrategyContext()

    context.set(
        "price",
        100,
    )

    assert context.contains(
        "price"
    )


def test_remove():
    context = StrategyContext()

    context.set(
        "price",
        100,
    )

    context.remove(
        "price"
    )

    assert context.contains(
        "price"
    ) is False


def test_clear():
    context = StrategyContext()

    context.set(
        "a",
        1,
    )

    context.set(
        "b",
        2,
    )

    context.clear()

    assert context.is_empty()


def test_keys():
    context = StrategyContext()

    context.set(
        "a",
        1,
    )

    context.set(
        "b",
        2,
    )

    assert context.keys() == [
        "a",
        "b",
    ]


def test_values():
    context = StrategyContext()

    context.set(
        "a",
        1,
    )

    context.set(
        "b",
        2,
    )

    assert context.values() == [
        1,
        2,
    ]


def test_items():
    context = StrategyContext()

    context.set(
        "a",
        1,
    )

    context.set(
        "b",
        2,
    )

    assert context.items() == [
        ("a", 1),
        ("b", 2),
    ]


def test_size():
    context = StrategyContext()

    context.set(
        "a",
        1,
    )

    context.set(
        "b",
        2,
    )

    assert context.size() == 2


def test_empty():
    context = StrategyContext()

    assert context.is_empty()
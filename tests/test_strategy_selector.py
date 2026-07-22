from portfolio.strategy_manager import StrategyManager
from portfolio.strategy_selector import StrategySelector


def test_create_strategy_selector():
    selector = StrategySelector()

    assert selector is not None


def test_selector_has_strategy_manager():
    selector = StrategySelector()

    assert isinstance(
        selector.manager,
        StrategyManager,
    )


def test_select_strategy():
    selector = StrategySelector()

    selector.select("ORB")

    assert selector.selected_strategy == "ORB"


def test_get_selected_strategy():
    selector = StrategySelector()

    selector.select("VWAP")

    assert selector.get_selected() == "VWAP"


def test_clear_selected_strategy():
    selector = StrategySelector()

    selector.select("ORB")

    selector.clear_selection()

    assert selector.get_selected() is None


def test_select_multiple_strategies():
    selector = StrategySelector()

    selector.manager.register(
        "ORB",
        object(),
    )
    selector.manager.register(
        "VWAP",
        object(),
    )

    selector.select_many(
        [
            "ORB",
            "VWAP",
        ]
    )

    assert selector.get_selected_many() == [
        "ORB",
        "VWAP",
    ]


def test_select_many_filters_unregistered():
    selector = StrategySelector()

    selector.manager.register(
        "ORB",
        object(),
    )

    selector.select_many(
        [
            "ORB",
            "INVALID",
        ]
    )

    assert selector.get_selected_many() == [
        "ORB",
    ]


def test_get_selected_objects():
    selector = StrategySelector()

    orb = object()
    vwap = object()

    selector.manager.register(
        "ORB",
        orb,
    )
    selector.manager.register(
        "VWAP",
        vwap,
    )

    selector.select_many(
        [
            "ORB",
            "VWAP",
        ]
    )

    assert selector.get_selected_objects() == [
        orb,
        vwap,
    ]


def test_has_selected_strategies():
    selector = StrategySelector()

    assert selector.has_selected() is False

    selector.manager.register(
        "ORB",
        object(),
    )

    selector.select_many(
        [
            "ORB",
        ]
    )

    assert selector.has_selected() is True


def test_clear_selected_many():
    selector = StrategySelector()

    selector.manager.register(
        "ORB",
        object(),
    )

    selector.select_many(
        [
            "ORB",
        ]
    )

    assert selector.has_selected() is True

    selector.clear_selected_many()

    assert selector.has_selected() is False
    assert selector.get_selected_many() == []


class DummyExecStrategy:
    def execute(self):
        return "BUY"


def test_execute_selected():
    selector = StrategySelector()

    strategy = DummyExecStrategy()

    selector.manager.register(
        "ORB",
        strategy,
    )
    selector.manager.enable(
        "ORB",
    )

    selector.select_many(
        [
            "ORB",
        ]
    )

    assert selector.execute_selected() == {
        "ORB": "BUY",
    }


def test_selected_count():
    selector = StrategySelector()

    assert selector.selected_count() == 0

    selector.manager.register(
        "ORB",
        object(),
    )
    selector.manager.register(
        "VWAP",
        object(),
    )

    selector.select_many(
        [
            "ORB",
            "VWAP",
        ]
    )

    assert selector.selected_count() == 2


def test_is_selected():
    selector = StrategySelector()

    selector.manager.register(
        "ORB",
        object(),
    )
    selector.manager.register(
        "VWAP",
        object(),
    )

    selector.select_many(
        [
            "ORB",
        ]
    )

    assert selector.is_selected("ORB") is True
    assert selector.is_selected("VWAP") is False


def test_remove_selected_strategy():
    selector = StrategySelector()

    selector.manager.register(
        "ORB",
        object(),
    )
    selector.manager.register(
        "VWAP",
        object(),
    )

    selector.select_many(
        [
            "ORB",
            "VWAP",
        ]
    )

    selector.remove_selected("ORB")

    assert selector.get_selected_many() == [
        "VWAP",
    ]


def test_select_all():
    selector = StrategySelector()

    selector.manager.register(
        "ORB",
        object(),
    )
    selector.manager.register(
        "VWAP",
        object(),
    )

    selector.select_all()

    assert selector.get_selected_many() == [
        "ORB",
        "VWAP",
    ]

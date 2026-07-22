from portfolio.strategy_allocator import StrategyAllocator
from portfolio.strategy_registry import StrategyRegistry
from portfolio.strategy_manager import StrategyManager
from portfolio.strategy_selector import StrategySelector


class FakeStrategy:

    def __init__(self, value="OK"):
        self.value = value

    def execute(self):
        return self.value


# -------------------------
# Strategy Allocator
# -------------------------


def test_strategy_allocator_initial_capital():

    allocator = StrategyAllocator(100000)

    assert allocator.total_capital == 100000


def test_allocate_strategy_capital():

    allocator = StrategyAllocator(100000)

    result = allocator.allocate(
        "NIFTY",
        20000,
    )

    assert result == 20000


def test_allocator_prevents_negative():

    allocator = StrategyAllocator(100000)

    assert allocator.allocate(
        "NIFTY",
        -100,
    ) == 0


def test_allocator_limits_amount():

    allocator = StrategyAllocator(100000)

    assert allocator.allocate(
        "NIFTY",
        200000,
    ) == 100000


def test_allocator_release():

    allocator = StrategyAllocator(100000)

    allocator.allocate(
        "NIFTY",
        20000,
    )

    assert allocator.release("NIFTY") == 20000


def test_allocator_utilization():

    allocator = StrategyAllocator(100000)

    allocator.allocate(
        "NIFTY",
        50000,
    )

    assert allocator.utilization() == 50


# -------------------------
# Registry
# -------------------------


def test_register_strategy():

    registry = StrategyRegistry()

    registry.register(
        "S1",
        FakeStrategy(),
    )

    assert registry.contains("S1")


def test_get_strategy():

    registry = StrategyRegistry()

    strategy = FakeStrategy()

    registry.register(
        "S1",
        strategy,
    )

    assert registry.get("S1") == strategy


def test_unregister_strategy():

    registry = StrategyRegistry()

    registry.register(
        "S1",
        FakeStrategy(),
    )

    registry.unregister("S1")

    assert not registry.contains("S1")


def test_list_strategies():

    registry = StrategyRegistry()

    registry.register(
        "S1",
        FakeStrategy(),
    )

    assert "S1" in registry.list_strategies()


# -------------------------
# Strategy Manager
# -------------------------


def test_manager_register():

    manager = StrategyManager()

    manager.register(
        "S1",
        FakeStrategy(),
    )

    assert manager.get("S1") is not None


def test_enable_strategy():

    manager = StrategyManager()

    manager.enable("S1")

    assert manager.is_enabled("S1")


def test_disable_strategy():

    manager = StrategyManager()

    manager.enable("S1")

    manager.disable("S1")

    assert not manager.is_enabled("S1")


def test_execute_strategy():

    manager = StrategyManager()

    manager.register(
        "S1",
        FakeStrategy("DONE"),
    )

    manager.enable("S1")

    assert manager.execute("S1") == "DONE"


# -------------------------
# Strategy Selector
# -------------------------


def test_select_strategy():

    selector = StrategySelector()

    selector.select("S1")

    assert selector.get_selected() == "S1"


def test_clear_selection():

    selector = StrategySelector()

    selector.select("S1")

    selector.clear_selection()

    assert selector.get_selected() is None


def test_select_many():

    selector = StrategySelector()

    selector.manager.register(
        "A",
        FakeStrategy(),
    )

    selector.select_many(
        ["A", "B"]
    )

    assert selector.get_selected_many() == ["A"]


def test_selected_count():

    selector = StrategySelector()

    selector.selected_strategies = [
        "A",
        "B",
    ]

    assert selector.selected_count() == 2


def test_select_all():

    selector = StrategySelector()

    selector.manager.register(
        "A",
        FakeStrategy(),
    )

    selector.select_all()

    assert selector.is_selected("A")
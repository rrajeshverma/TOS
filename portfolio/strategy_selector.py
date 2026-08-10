from portfolio.strategy_manager import StrategyManager


class StrategySelector:
    def __init__(
        self,
    ):
        self.manager = StrategyManager()
        self.selected_strategy = None
        self.selected_strategies = []

    def select(
        self,
        name,
    ):
        self.selected_strategy = name

    def get_selected(
        self,
    ):
        return self.selected_strategy

    def clear_selection(
        self,
    ):
        self.selected_strategy = None

    def select_many(
        self,
        names,
    ):
        self.selected_strategies = [name for name in names if self.manager.registry.contains(name)]

    def get_selected_many(
        self,
    ):
        return self.selected_strategies

    def get_selected_objects(
        self,
    ):
        return [self.manager.get(name) for name in self.selected_strategies]

    def has_selected(
        self,
    ):
        return bool(self.selected_strategies)

    def clear_selected_many(
        self,
    ):
        self.selected_strategies.clear()

    def execute_selected(
        self,
    ):
        results = {}

        for name in self.selected_strategies:
            results[name] = self.manager.execute(name)

        return results

    def selected_count(
        self,
    ):
        return len(self.selected_strategies)

    def is_selected(
        self,
        name,
    ):
        return name in self.selected_strategies

    def remove_selected(
        self,
        name,
    ):
        if name in self.selected_strategies:
            self.selected_strategies.remove(name)

    def select_all(
        self,
    ):
        self.selected_strategies = self.manager.registry.list_strategies()

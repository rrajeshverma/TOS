from optimizer.search_manager import SearchManager


def test_create_search_manager():
    manager = SearchManager()

    assert manager is not None


def test_execute_search():
    class DummySearch:
        def run(self, evaluator):
            return "completed"

    manager = SearchManager()

    result = manager.run(
        DummySearch(),
        lambda x: x,
    )

    assert result == "completed"


def test_best_result():
    class DummySearch:
        def best_result(self):
            return "best"

    manager = SearchManager()

    assert manager.best_result(DummySearch()) == "best"

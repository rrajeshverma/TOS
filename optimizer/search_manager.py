class SearchManager:
    def run(self, search, evaluator):
        return search.run(evaluator)

    def best_result(self, search):
        return search.best_result()

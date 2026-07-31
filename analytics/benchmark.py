class Benchmark:
    def outperformed(
        self,
        strategy_return,
        benchmark_return,
    ):
        return strategy_return > benchmark_return

    def excess_return(
        self,
        strategy_return,
        benchmark_return,
    ):
        return strategy_return - benchmark_return

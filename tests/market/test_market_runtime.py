from market.market_runtime import MarketRuntime


def test_market_runtime_initial_state():

    runtime = MarketRuntime()

    assert runtime is not None


def test_market_runtime_processes_tick():

    class Feed:
        pass

    runtime = MarketRuntime(
        feed=Feed()
    )

    assert runtime.feed is not None

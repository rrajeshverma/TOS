from portfolio.strategy_scheduler import StrategyScheduler


class DummyPipeline:
    def execute(self, context=None):
        return ["BUY", "SELL"]


def test_create_scheduler():
    scheduler = StrategyScheduler()

    assert scheduler is not None


def test_enabled_by_default():
    scheduler = StrategyScheduler()

    assert scheduler.is_enabled()


def test_disable():
    scheduler = StrategyScheduler()

    scheduler.disable()

    assert scheduler.is_enabled() is False


def test_enable():
    scheduler = StrategyScheduler()

    scheduler.disable()
    scheduler.enable()

    assert scheduler.is_enabled()


def test_should_run():
    scheduler = StrategyScheduler()

    assert scheduler.should_run()


def test_should_not_run():
    scheduler = StrategyScheduler()

    scheduler.disable()

    assert scheduler.should_run() is False


def test_run_pipeline():
    scheduler = StrategyScheduler()

    pipeline = DummyPipeline()

    assert scheduler.run(pipeline) == [
        "BUY",
        "SELL",
    ]


def test_run_disabled():
    scheduler = StrategyScheduler()

    scheduler.disable()

    pipeline = DummyPipeline()

    assert scheduler.run(pipeline) == []
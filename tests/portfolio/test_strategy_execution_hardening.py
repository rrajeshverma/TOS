from portfolio.strategy_executor import StrategyExecutor
from portfolio.strategy_pipeline import StrategyPipeline
from portfolio.strategy_scheduler import StrategyScheduler
from portfolio.strategy_validator import StrategyValidator
from portfolio.strategy_lifecycle import StrategyLifecycle


class FakeStrategy:
    def __init__(self):
        self.calls = 0
        self.initialized = False
        self.shutdown_called = False

    def execute(self, context=None):
        self.calls += 1
        return "RESULT"

    def initialize(self):
        self.initialized = True

    def shutdown(self):
        self.shutdown_called = True


# -------------------------
# Executor
# -------------------------


def test_executor_runs_strategy():
    strategy = FakeStrategy()

    result = StrategyExecutor().execute(strategy)

    assert result == "RESULT"


def test_executor_with_context():
    strategy = FakeStrategy()

    StrategyExecutor().execute(
        strategy,
        {"x": 1},
    )

    assert strategy.calls == 1


def test_execute_many():
    strategies = [
        FakeStrategy(),
        FakeStrategy(),
    ]

    result = StrategyExecutor().execute_many(strategies)

    assert len(result) == 2


def test_execute_first():
    strategies = [
        FakeStrategy(),
        FakeStrategy(),
    ]

    assert StrategyExecutor().execute_first(strategies) == "RESULT"


def test_execute_empty_first():
    assert StrategyExecutor().execute_first([]) is None


# -------------------------
# Pipeline
# -------------------------


def test_pipeline_add():
    pipeline = StrategyPipeline()

    strategy = FakeStrategy()

    pipeline.add(strategy)

    assert pipeline.count() == 1


def test_pipeline_remove():
    pipeline = StrategyPipeline()

    strategy = FakeStrategy()

    pipeline.add(strategy)
    pipeline.remove(strategy)

    assert pipeline.is_empty()


def test_pipeline_execute():
    pipeline = StrategyPipeline()

    pipeline.add(FakeStrategy())

    assert pipeline.execute() == ["RESULT"]


def test_pipeline_first():
    pipeline = StrategyPipeline()

    strategy = FakeStrategy()

    pipeline.add(strategy)

    assert pipeline.first() == strategy


# -------------------------
# Scheduler
# -------------------------


def test_scheduler_disabled():
    scheduler = StrategyScheduler()

    scheduler.disable()

    assert scheduler.should_run() is False


def test_scheduler_runs_pipeline():
    scheduler = StrategyScheduler()

    pipeline = StrategyPipeline()

    pipeline.add(FakeStrategy())

    assert scheduler.run(pipeline) == ["RESULT"]


def test_scheduler_enable():
    scheduler = StrategyScheduler()

    scheduler.disable()
    scheduler.enable()

    assert scheduler.is_enabled()


# -------------------------
# Validator
# -------------------------


def test_validator_name():
    assert StrategyValidator().is_valid_name("NIFTY")


def test_validator_invalid_name():
    assert not StrategyValidator().is_valid_name("")


def test_validator_strategy():
    assert StrategyValidator().is_valid_strategy(FakeStrategy())


def test_validator_full_validation():
    assert StrategyValidator().validate("S1", FakeStrategy())


# -------------------------
# Lifecycle
# -------------------------


def test_lifecycle_start():
    lifecycle = StrategyLifecycle()

    lifecycle.start()

    assert lifecycle.is_started()


def test_lifecycle_restart():
    lifecycle = StrategyLifecycle()

    lifecycle.restart()

    assert lifecycle.is_started()


def test_lifecycle_initialize():
    strategy = FakeStrategy()

    StrategyLifecycle().initialize(strategy)

    assert strategy.initialized


def test_lifecycle_shutdown():
    strategy = FakeStrategy()

    StrategyLifecycle().shutdown(strategy)

    assert strategy.shutdown_called

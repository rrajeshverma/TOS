from portfolio.strategy_lifecycle import StrategyLifecycle


class DummyStrategy:
    def __init__(self):
        self.initialized = False
        self.stopped = False

    def initialize(self):
        self.initialized = True

    def shutdown(self):
        self.stopped = True


def test_create():
    lifecycle = StrategyLifecycle()

    assert lifecycle is not None


def test_initialize():
    lifecycle = StrategyLifecycle()
    strategy = DummyStrategy()

    lifecycle.initialize(strategy)

    assert strategy.initialized


def test_start():
    lifecycle = StrategyLifecycle()

    lifecycle.start()

    assert lifecycle.is_started()


def test_stop():
    lifecycle = StrategyLifecycle()

    lifecycle.start()
    lifecycle.stop()

    assert lifecycle.is_started() is False


def test_restart():
    lifecycle = StrategyLifecycle()

    lifecycle.restart()

    assert lifecycle.is_started()


def test_shutdown():
    lifecycle = StrategyLifecycle()
    strategy = DummyStrategy()

    lifecycle.shutdown(strategy)

    assert strategy.stopped

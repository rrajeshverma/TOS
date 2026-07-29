from unittest.mock import Mock

from services.paper_trade_runner import PaperTradeRunner
from shared.enums import Signal


class FakeDecision:
    def __init__(self):
        self.signal = Signal.BUY_CE


class FakeRisk:
    def __init__(self, approved=True):
        self.is_approved = approved
        self.reasons = ("Risk rejected",)


class FakeTrade:
    def __init__(self):
        self.trade_id = "TRADE001"


class FakeOrder:
    def __init__(self):
        self.order_id = "ORDER001"
        self.quantity = 65


class FakePosition:
    def __init__(self):
        self.position_id = "POSITION001"


def create_runner():
    strategy = Mock()
    broker = Mock()
    adapter = Mock()

    runner = PaperTradeRunner(
        strategy,
        broker,
        adapter,
    )

    return runner, strategy, adapter


def test_run_returns_rejected_when_risk_not_approved():
    runner, strategy, adapter = create_runner()

    strategy.decide.return_value = FakeDecision()

    runner.risk_engine = Mock()
    runner.risk_engine.evaluate.return_value = FakeRisk(False)

    result = runner.run()

    assert result["status"] == "REJECTED"
    assert result["reason"] == ("Risk rejected",)


def test_strategy_engine_called_once():
    runner, strategy, adapter = create_runner()

    strategy.decide.return_value = FakeDecision()

    runner.risk_engine = Mock()
    runner.risk_engine.evaluate.return_value = FakeRisk()

    runner.trade_factory = Mock()
    runner.trade_factory.create.return_value = FakeTrade()

    runner.order_factory = Mock()
    runner.order_factory.create.return_value = FakeOrder()

    runner.position_manager = Mock()
    runner.position_manager.open_position.return_value = FakePosition()

    adapter.to_execution_order.return_value = object()
    adapter.execute.return_value = "OK"

    runner.run()

    strategy.decide.assert_called_once()


def test_adapter_execute_called_once():
    runner, strategy, adapter = create_runner()

    strategy.decide.return_value = FakeDecision()

    runner.risk_engine = Mock()
    runner.risk_engine.evaluate.return_value = FakeRisk()

    runner.trade_factory = Mock()
    runner.trade_factory.create.return_value = FakeTrade()

    runner.order_factory = Mock()
    runner.order_factory.create.return_value = FakeOrder()

    runner.position_manager = Mock()
    runner.position_manager.open_position.return_value = FakePosition()

    adapter.to_execution_order.return_value = object()
    adapter.execute.return_value = "BROKER_OK"

    runner.run()

    adapter.execute.assert_called_once()


def test_run_returns_expected_fields():
    runner, strategy, adapter = create_runner()

    strategy.decide.return_value = FakeDecision()

    runner.risk_engine = Mock()
    runner.risk_engine.evaluate.return_value = FakeRisk()

    runner.trade_factory = Mock()
    runner.trade_factory.create.return_value = FakeTrade()

    runner.order_factory = Mock()
    runner.order_factory.create.return_value = FakeOrder()

    runner.position_manager = Mock()
    runner.position_manager.open_position.return_value = FakePosition()

    adapter.to_execution_order.return_value = object()
    adapter.execute.return_value = "SUCCESS"

    result = runner.run()

    assert result["signal"] == Signal.BUY_CE
    assert result["trade_id"] == "TRADE001"
    assert result["order_id"] == "ORDER001"
    assert result["broker_result"] == "SUCCESS"
    assert result["position_id"] == "POSITION001"


def test_position_manager_called_once():
    runner, strategy, adapter = create_runner()

    strategy.decide.return_value = FakeDecision()

    runner.risk_engine = Mock()
    runner.risk_engine.evaluate.return_value = FakeRisk()

    trade = FakeTrade()
    order = FakeOrder()

    runner.trade_factory = Mock()
    runner.trade_factory.create.return_value = trade

    runner.order_factory = Mock()
    runner.order_factory.create.return_value = order

    runner.position_manager = Mock()
    runner.position_manager.open_position.return_value = FakePosition()

    adapter.to_execution_order.return_value = object()
    adapter.execute.return_value = "OK"

    runner.run()

    runner.position_manager.open_position.assert_called_once_with(
        order,
        order.quantity,
        100,
    )

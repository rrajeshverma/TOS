from integration.engine_context import EngineContext
from integration.trading_engine import TradingEngine


class FakeMarketEngine:
    def __init__(self):
        self.called = False

    def run(self):
        self.called = True
        return []


class FakeIndicatorEngine:
    def run(self, candles):
        return candles


class FakeStrategyEngine:
    def run(self, indicators):
        return indicators


class FakeDecisionEngine:
    def run(self, data):
        return []


class FakeRiskEngine:
    def run(self, signals):
        return signals


class FakeTradeFactory:
    def __init__(self):
        self.called = False

    def create(self, trade_plan):
        self.called = True
        return {"trade": "BUY"}


class FakePaperTradingService:
    def run(self, trades):
        return trades


class FakePositionManager:
    def run(self, trades):
        return trades


class FakeTradeJournal:
    def run(self, trades):
        return True


def test_full_trading_day():
    market = FakeMarketEngine()

    context = EngineContext(
        market_engine=market,
        indicator_engine=FakeIndicatorEngine(),
        strategy_engine=FakeStrategyEngine(),
        decision_engine=FakeDecisionEngine(),
        risk_engine=FakeRiskEngine(),
        trade_factory=FakeTradeFactory(),
        paper_trading_service=None,
        position_manager=None,
        trade_journal=None,
    )

    engine = TradingEngine(context)

    trade = engine.run()

    assert market.called
    assert context.trade_factory.called
    assert trade == {"trade": "BUY"}
from integration.engine_context import EngineContext


class TradingEngine:
    """
    Trading Engine

    Pipeline

        MarketEngine
              │
              ▼
        IndicatorEngine
              │
              ▼
        StrategyEngine
              │
              ▼
        DecisionEngine
              │
              ▼
        RiskEngine

    Future

        TradeFactory
              │
              ▼
        PaperTradingService
              │
              ▼
        PositionManager
              │
              ▼
        TradeJournal
    """

    def __init__(self, context: EngineContext):
        self.context = context

    def run(self):
        # Step 1
        market_data = self.context.market_engine.run()

        # Step 2
        indicators = self.context.indicator_engine.run(market_data)

        # Step 3
        strategy_signal = self.context.strategy_engine.run(indicators)

        # Step 4
        decision = self.context.decision_engine.run(strategy_signal)

        # Step 5
        trade_plan = self.context.risk_engine.run(decision)

        return trade_plan
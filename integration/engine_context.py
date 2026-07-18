class EngineContext:
    def __init__(
        self,
        market_engine,
        indicator_engine,
        strategy_engine,
        decision_engine,
        risk_engine,
        trade_factory,
        paper_trading_service,
        position_manager,
        trade_journal,
    ):
        self.market_engine = market_engine
        self.indicator_engine = indicator_engine
        self.strategy_engine = strategy_engine
        self.decision_engine = decision_engine
        self.risk_engine = risk_engine
        self.trade_factory = trade_factory
        self.paper_trading_service = paper_trading_service
        self.position_manager = position_manager
        self.trade_journal = trade_journal
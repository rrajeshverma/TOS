from integration.engine_context import EngineContext


def test_engine_context_stores_dependencies():

    market = object()
    indicator = object()
    strategy = object()
    decision = object()
    risk = object()
    trade_factory = object()
    paper = object()
    position = object()
    journal = object()

    context = EngineContext(
        market,
        indicator,
        strategy,
        decision,
        risk,
        trade_factory,
        paper,
        position,
        journal,
    )

    assert context.market_engine is market
    assert context.indicator_engine is indicator
    assert context.strategy_engine is strategy
    assert context.decision_engine is decision
    assert context.risk_engine is risk
    assert context.trade_factory is trade_factory
    assert context.paper_trading_service is paper
    assert context.position_manager is position
    assert context.trade_journal is journal

from runtime.trading_pipeline import TradingPipeline


class Dummy:
    pass


def test_constructor():
    pipeline = TradingPipeline(
        market_engine=Dummy(),
        indicator_engine=Dummy(),
        decision_engine=Dummy(),
        trade_quality_engine=Dummy(),
        risk_engine=Dummy(),
        position_sizing_engine=Dummy(),
        trade_planning_engine=Dummy(),
        trade_management_engine=Dummy(),
    )

    assert pipeline is not None

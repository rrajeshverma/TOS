from strategies.strategy_metadata import StrategyMetadata


def test_metadata_creation():
    metadata = StrategyMetadata(
        name="EMA",
        version="1.0.0",
        author="Rajesh Varma",
        market="NIFTY",
        timeframe="5m",
    )

    assert metadata.name == "EMA"
    assert metadata.version == "1.0.0"
    assert metadata.author == "Rajesh Varma"
    assert metadata.market == "NIFTY"
    assert metadata.timeframe == "5m"
    assert metadata.enabled is True


def test_metadata_can_be_disabled():
    metadata = StrategyMetadata(
        name="EMA",
        version="1.0.0",
        author="Rajesh Varma",
        market="NIFTY",
        timeframe="5m",
        enabled=False,
    )

    assert metadata.enabled is False


def test_metadata_is_immutable():
    metadata = StrategyMetadata(
        name="EMA",
        version="1.0.0",
        author="Rajesh Varma",
        market="NIFTY",
        timeframe="5m",
    )

    try:
        metadata.name = "ORB"
        assert False, "Expected frozen dataclass"
    except Exception:
        pass

import pytest

from strategies.base_strategy import BaseStrategy
from strategies.strategy_metadata import StrategyMetadata
from strategies.strategy_plugin_validator import StrategyPluginValidator


class ValidStrategy(BaseStrategy):
    metadata = StrategyMetadata(
        name="EMA",
        version="1.0.0",
        author="Rajesh Varma",
        market="NIFTY",
        timeframe="5m",
    )

    def name(self):
        return self.metadata.name

    def analyze(self, market):
        return market

    def generate_signal(self, market):
        return "BUY"


class MissingMetadataStrategy(BaseStrategy):
    def name(self):
        return "Invalid"

    def analyze(self, market):
        return market

    def generate_signal(self, market):
        return "BUY"


def test_valid_strategy_passes():
    assert StrategyPluginValidator().validate(ValidStrategy())


def test_missing_metadata_fails():
    with pytest.raises(ValueError, match="metadata"):
        StrategyPluginValidator().validate(
            MissingMetadataStrategy()
        )

class EmptyAuthorStrategy(BaseStrategy):
    metadata = StrategyMetadata(
        name="EMA",
        version="1.0.0",
        author="",
        market="NIFTY",
        timeframe="5m",
    )

    def name(self):
        return self.metadata.name

    def analyze(self, market):
        return market

    def generate_signal(self, market):
        return "BUY"


class InvalidEnabledStrategy(BaseStrategy):
    metadata = StrategyMetadata(
        name="EMA",
        version="1.0.0",
        author="Rajesh Varma",
        market="NIFTY",
        timeframe="5m",
        enabled="yes",  # intentionally invalid
    )

    def name(self):
        return self.metadata.name

    def analyze(self, market):
        return market

    def generate_signal(self, market):
        return "BUY"


def test_empty_author_fails():
    with pytest.raises(ValueError, match="author"):
        StrategyPluginValidator().validate(
            EmptyAuthorStrategy()
        )


def test_invalid_enabled_type_fails():
    with pytest.raises(TypeError, match="enabled"):
        StrategyPluginValidator().validate(
            InvalidEnabledStrategy()
        )
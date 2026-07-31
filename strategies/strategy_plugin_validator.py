from strategies.base_strategy import BaseStrategy
from strategies.strategy_metadata import StrategyMetadata


class StrategyPluginValidator:
    """
    Validates strategy plugin implementations.
    """

    def validate(self, strategy: BaseStrategy) -> bool:
        if not isinstance(strategy, BaseStrategy):
            raise TypeError("strategy must inherit from BaseStrategy")

        metadata = getattr(strategy, "metadata", None)

        if metadata is None:
            raise ValueError("Strategy metadata is required")

        if not isinstance(metadata, StrategyMetadata):
            raise TypeError("metadata must be a StrategyMetadata instance")

        required_fields = {
            "name": metadata.name,
            "version": metadata.version,
            "author": metadata.author,
            "market": metadata.market,
            "timeframe": metadata.timeframe,
        }

        for field_name, value in required_fields.items():
            if not isinstance(value, str):
                raise TypeError(f"Strategy {field_name} must be a string")

            if not value.strip():
                raise ValueError(f"Strategy {field_name} is required")

        if not isinstance(metadata.enabled, bool):
            raise TypeError("Strategy enabled must be a boolean")

        return True

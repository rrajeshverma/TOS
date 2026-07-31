from domain.indicator_set import IndicatorSet
from market.market_runtime import MarketRuntime


class IndicatorEngine:
    """Calculates technical indicators."""

    def calculate(self, runtime: MarketRuntime) -> IndicatorSet:
        if runtime is None:
            raise ValueError("runtime cannot be None")

        if not isinstance(runtime, MarketRuntime):
            raise TypeError("runtime must be MarketRuntime")

        return IndicatorSet(
            ema_high=0.0,
            ema_low=0.0,
            vwap=0.0,
            rsi=50.0,
            volume_average=0.0,
        )

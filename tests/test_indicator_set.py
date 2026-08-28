from domain.indicator_set import IndicatorSet

indicator = IndicatorSet(
    ema_high=24152.30,
    ema_low=24134.70,
    vwap=24120.10,
    rsi=58.75,
)

print(indicator)

print(indicator.is_bullish)

print(indicator.is_bearish)

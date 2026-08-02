# TOS Trading Rulebook

## Entry Rules
- Trading only between 10:15 and 14:30
- Price above EMA High
- Price above VWAP
- RSI > 55 (BUY CE)
- RSI < 45 (BUY PE)
- Ignore RSI between 45 and 55

## Entry Filters
- Skip abnormal breakout candles
- Don't chase extended moves away from EMA
- Require acceptable risk/reward
- Maximum 2 trades per day
- Stop trading after daily loss limit

## Exit Rules
- Structural stop-loss (EMA / Previous Candle)
- Target or trailing exit
- Force exit before market close

## Principle 11 - Respect Market Structure

- TOS never places a stop-loss at an arbitrary number of points.
- Stop-loss must be derived from market structure.
- Preferred order:
    1. Swing High / Swing Low
    2. Previous Candle High / Low
    3. EMA Support / Resistance
- A trade remains valid while the underlying market structure remains valid.
- A break of market structure invalidates the original trade idea.
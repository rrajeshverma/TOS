# Trading Operating System (TOS)

# NIFTY Weekly Options Strategy v1.0

---

## Objective

Trade NIFTY Weekly ITM Options using trend, momentum and institutional confirmation while maintaining strict risk management.

---

# Instrument

Underlying
    NIFTY 50 Index

Options
    Weekly Expiry

Strike Selection
    1 Strike ITM

Trading Style
    Intraday

Timeframe
    5 Minutes

---

# Trading Window

Entry Allowed

10:15 AM
↓

2:30 PM

No new trades after 2:30 PM.

All open positions must be closed before market close.

---

# Indicators

1. 33 EMA High

2. 33 EMA Low

3. VWAP

4. RSI

---

# BUY (CALL OPTION)

All conditions must be TRUE.

✓ Price closes above 33 EMA High

✓ RSI > 55

✓ Price above VWAP

✓ Trading time between
  10:15 and 14:30

✓ Maximum trades/day not exceeded

✓ Volatility Filter passes

✓ Stop Loss Filter passes

---

# SELL (PUT OPTION)

All conditions must be TRUE.

✓ Price closes below 33 EMA Low

✓ RSI < 45

✓ Price below VWAP

✓ Trading time between
  10:15 and 14:30

✓ Maximum trades/day not exceeded

✓ Volatility Filter passes

✓ Stop Loss Filter passes

---

# NO TRADE

No trade when

45 ≤ RSI ≤ 55

---

# Maximum Trades

Maximum

2 Trades per Day

No further entries after two completed trades.

---

# Stop Loss

BUY

Stop Loss =
Minimum of

• Previous Candle Low

OR

• 33 EMA Low

SELL

Stop Loss =
Maximum of

• Previous Candle High

OR

• 33 EMA High

---

# Target

Risk : Reward

1 : 2

---

# Trailing Stop

When trade reaches

+1R

↓

Move Stop Loss to Entry Price

Continue holding

↓

Exit at +2R

OR

Stop Loss

---

# Volatility Filter

Reject trade when

Current Candle Range

>

1.5 × Average Range of Last 10 Candles

---

# Maximum Stop Loss

Reject trade when calculated stop loss

>

30 NIFTY Points

---

# VWAP Distance Filter

Reject trade when price is excessively extended from VWAP.

(Default implementation threshold: 0.5%)

---

# Entry Timing Rule

Trade only on the first valid breakout signal.

Ignore delayed entries after multiple candles.

---

# Force Exit

Close all open positions before market close.

No overnight positions.

---

# Risk Management

Maximum Trades

2

Maximum Open Position

1

No Averaging

Allowed

No Martingale

Allowed

---

# Trade Journal

Every completed trade must record

Timestamp

Symbol

Option Type

Strike

Entry Price

Exit Price

Stop Loss

Target

Quantity

PnL

Strategy

Trade Duration

Exit Reason

Broker Order ID

---

# Future Enhancements (Not Part of v1.0)

• ADX Trend Strength Filter

• ATR Based Position Sizing

• Multi-Timeframe Confirmation

• Dynamic Trailing Stop

• Volatility Regime Detection

• Market Breadth Filter

---

# Version History

Version

1.0

Status

Frozen

This document defines the official trading rules for
Trading Operating System (TOS) Version 1.0.

Any modification to strategy rules must result in a new
strategy version.

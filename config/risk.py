"""
=========================================================
Trading Operating System (TOS)
Module      : Risk Configuration
Version     : 1.0.0
Author       : Rajesh Varma
Description : Centralized risk management settings.
=========================================================
"""

from decimal import Decimal

# =====================================================
# Capital
# =====================================================

CAPITAL = Decimal("100000")

# =====================================================
# Risk
# =====================================================

RISK_PERCENT = Decimal("2")

MAX_RISK_PER_TRADE = Decimal("2000")

MAX_DAILY_LOSS = Decimal("5000")

MAX_TRADES_PER_DAY = 4

# =====================================================
# Position
# =====================================================

DEFAULT_NIFTY_QTY = 65

# =====================================================
# Target
# =====================================================

RISK_REWARD_RATIO = Decimal("2")
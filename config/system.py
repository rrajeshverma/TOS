"""
=========================================================
Trading Operating System (TOS)
Module      : System Configuration
Version     : 1.0.0
Author      : Rajesh Varma
Description : Global system configuration for TOS.
=========================================================
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# =========================================================
# PROJECT
# =========================================================

PROJECT_NAME = "Trading Operating System"

PROJECT_CODE = "TOS"

VERSION = "1.0.0"

MODE = "PAPER"

BROKER = "DHAN"

# =========================================================
# DHAN API
# =========================================================

DHAN_CLIENT_ID = os.getenv("DHAN_CLIENT_ID")

DHAN_ACCESS_TOKEN = os.getenv("DHAN_ACCESS_TOKEN")


# =========================================================
# PATHS
# =========================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = ROOT_DIR / "data"

LOG_DIR = ROOT_DIR / "logs"

REPORT_DIR = ROOT_DIR / "reports_output"

DOCUMENT_DIR = ROOT_DIR / "docs"

# Create folders automatically

for folder in (
    DATA_DIR,
    LOG_DIR,
    REPORT_DIR,
):
    folder.mkdir(parents=True, exist_ok=True)

# =========================================================
# CAPITAL
# =========================================================

CAPITAL = 100000.00

RISK_PERCENT = 2.0

MAX_DAILY_LOSS = 8000.00

MAX_TRADES_PER_DAY = 4

# =========================================================
# MARKET
# =========================================================

EXCHANGE = "NSE"

INDEX = "NIFTY"

TIMEFRAME = "5m"

SCAN_INTERVAL_SECONDS = 60

# =========================================================
# TRADING TIME
# =========================================================

ENTRY_START = "09:25"

LAST_ENTRY = "15:00"

FORCE_EXIT = "15:15"

# =========================================================
# STRATEGY
# =========================================================

EMA_PERIOD = 33

VWAP_ENABLED = True

RSI_PERIOD = 14

RSI_BUY = 55

RSI_SELL = 45

EMA_SL_BUFFER = 0.0

USE_TRAILING_SL = True

USE_DYNAMIC_POSITION_SIZE = True

# =========================================================
# LOGGING
# =========================================================

LOG_LEVEL = "INFO"

LOG_TO_FILE = True

LOG_TO_CONSOLE = True

# =========================================================
# REPORTS
# =========================================================

SAVE_DECISION_JOURNAL = True

SAVE_TRADE_JOURNAL = True

SAVE_DAILY_REPORT = True

SAVE_WEEKLY_REPORT = True

# =========================================================
# DEVELOPMENT
# =========================================================

DEBUG = False

TEST_MODE = False

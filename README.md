# Trading Operating System (TOS)

> **A production-oriented algorithmic trading platform built with Clean
> Architecture, Domain-Driven Design (DDD), SOLID principles, and
> Test-Driven Development (TDD).**

## Overview

Trading Operating System (TOS) is a modular algorithmic trading platform
designed to support the complete trading lifecycle---from market data
ingestion and strategy evaluation through risk management, order
execution, portfolio management, monitoring, and reporting.

### Highlights

-   Python 3.12+
-   Clean Architecture
-   SOLID Principles
-   Domain-Driven Design (DDD)
-   Test-Driven Development (TDD)
-   Historical Backtesting
-   Paper Trading
-   Live Trading Framework
-   5,217+ automated tests
-   Ruff clean

## Architecture

``` text
Market Data
    │
    ▼
Indicator Engine
    │
    ▼
Strategy Engine
    │
    ▼
Decision Engine
    │
    ▼
Risk Engine
    │
    ▼
Execution Manager
    │
    ▼
Broker Adapter
    │
    ▼
Portfolio / Positions
    │
    ▼
Journal / Reporting
```

## Repository Structure

``` text
analytics/
backtesting/
brokers/
config/
dashboard/
docs/
domain/
engines/
events/
execution/
journal/
market/
monitoring/
paper/
performance/
portfolio/
reporting/
risk/
runtime/
services/
storage/
tests/
validation/
```

## Installation

``` bash
git clone <repository-url>
cd TOS
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Quick Start

``` bash
python main.py
pytest
ruff check .
ruff format --check .
```

## Documentation

See: - docs/architecture.md - docs/deployment.md - docs/API.md -
docs/strategy_development.md - docs/TRADING_RULEBOOK.md -
docs/ReleaseNotes.md

## Development Workflow

1.  Write tests.
2.  Implement changes.
3.  Run the full test suite.
4.  Run Ruff.
5.  Commit only with a clean repository.

## Current Status

-   5,217+ tests passing
-   0 failures
-   Ruff clean
-   Python 3.12+

## Roadmap

-   v2.5.0-beta1
-   Live Trading Readiness
-   Enhanced reporting
-   Operational dashboards

## License

Proprietary. All rights reserved.

# Trading Operating System (TOS)

A modular algorithmic trading platform built using **Clean Architecture**, **SOLID principles**, **Domain-Driven Design (DDD)**, and **Test-Driven Development (TDD)**.

---

## Overview

Trading Operating System (TOS) is designed to provide a scalable, maintainable, and extensible framework for developing, testing, and executing algorithmic trading strategies.

The platform supports:

- Historical Backtesting
- Paper Trading
- Strategy Optimization
- Portfolio Analytics
- Performance Reporting
- Risk Management
- Broker Integration
- Runtime Monitoring

---

## Architecture

The project follows:

- Clean Architecture
- SOLID Principles
- Domain-Driven Design (DDD)
- Test-Driven Development (TDD)

For more information, see:

```
docs/Architecture.md
```

---

## Project Structure

```
analytics/
backtesting/
brokers/
config/
dashboard/
domain/
engines/
events/
execution/
journal/
monitoring/
optimizer/
performance/
portfolio/
reporting/
risk/
services/
storage/
tests/
validation/
```

---

## Requirements

- Python 3.12+
- Linux (Ubuntu recommended)
- Virtual Environment

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd TOS
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install runtime dependencies:

```bash
pip install -r requirements.txt
```

Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

---

## Running Tests

Run the full test suite:

```bash
python -m pytest
```

---

## Code Quality

Formatting:

```bash
python -m black .
```

Import sorting:

```bash
python -m isort .
```

Linting:

```bash
python -m ruff check .
```

Coverage:

```bash
python -m pytest --cov=.
```

---

## Development Workflow

The project follows:

1. RED
2. GREEN
3. REFACTOR

Every production change is expected to include automated tests.

---

## Current Status

- Clean Architecture
- SOLID
- Domain-Driven Design
- Test-Driven Development
- 1505+ Passing Tests

---

## Roadmap

- Enhanced Reporting
- HTML/PDF Reports
- Portfolio Dashboard
- Multi-Strategy Execution
- Live Trading Enhancements

---

## License

Proprietary.
All rights reserved.
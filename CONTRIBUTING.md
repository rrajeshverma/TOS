# Contributing to Trading Operating System (TOS)

Thank you for contributing to the **Trading Operating System (TOS)** project.

TOS is built with a strong emphasis on software engineering principles, maintainability, reliability, and automated testing. Every contribution should preserve these standards.

---

# Engineering Principles

The project is built on the following principles:

* Clean Architecture
* SOLID Principles
* Domain-Driven Design (DDD)
* Test-Driven Development (TDD)

Business logic should remain independent from infrastructure and external services.

---

# Development Environment

## Requirements

* Python 3.12+
* Linux (Ubuntu recommended)
* Virtual Environment

Create and activate the environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

---

# Coding Standards

All new code should:

* Follow PEP 8.
* Include type hints where appropriate.
* Keep functions focused and concise.
* Prefer composition over unnecessary inheritance.
* Avoid duplicated logic.
* Maintain backward compatibility unless intentionally changed.

---

# Test-Driven Development

TOS follows a strict TDD workflow.

For every change:

1. Write or update tests.
2. Implement the change.
3. Ensure all tests pass.
4. Refactor if needed.
5. Verify no regressions.

Never merge code that breaks existing tests.

---

# Code Quality

Before committing, run:

```bash
pytest

ruff check .

ruff format --check .
```

Expected result:

* All tests passing
* Ruff check passes
* Ruff formatting passes

---

# Branch Strategy

Use the following branch naming convention:

```text
main
release/*
feature/*
hotfix/*
```

Examples:

```text
feature/paper-trading-v2
feature/runtime-monitor
release/v2.5.0
hotfix/order-routing
```

---

# Commit Message Convention

Use concise, descriptive commit messages.

Examples:

```text
feat: add execution retry logic
fix: resolve paper trading position sync
test: improve runtime coverage
docs: update README
refactor: simplify execution manager
```

---

# Pull Request Checklist

Before opening a pull request, verify:

* [ ] All tests pass.
* [ ] Ruff check passes.
* [ ] Ruff formatting passes.
* [ ] Documentation updated (if applicable).
* [ ] No unnecessary files included.
* [ ] No regression introduced.

---

# Documentation

When introducing new functionality, update the relevant documentation.

Documentation is maintained under the `docs/` directory.

Examples include:

* Architecture
* API Reference
* Deployment Guide
* Strategy Development
* Trading Rulebook
* Release Notes

---

# Project Philosophy

The primary objectives of TOS are:

* Reliability
* Maintainability
* Readability
* Testability
* Extensibility

Engineering quality always takes precedence over short-term feature velocity.

---

# Release Checklist

Before creating a release:

1. All automated tests pass.
2. Ruff check passes.
3. Ruff formatting passes.
4. Documentation is up to date.
5. Version numbers are synchronized.
6. CHANGELOG is updated.
7. Repository is clean.
8. Release tag is created.

---

# Thank You

Thank you for helping improve Trading Operating System (TOS).

Every contribution—whether code, documentation, testing, or review—helps strengthen the project and maintain its engineering standards.

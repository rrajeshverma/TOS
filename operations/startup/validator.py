"""
Startup Validation Framework

TOS v1.1.1
"""

from dataclasses import dataclass, field
from typing import Callable


@dataclass(slots=True, frozen=True)
class ValidationResult:
    """Result returned by StartupValidator."""
    success: bool = True


class StartupValidator:
    """Runs startup validation checks."""

    def __init__(self) -> None:
        self.checks: list[Callable[[], bool]] = []

    def register(self, check: Callable[[], bool]) -> None:
        """Register a validation check."""
        self.checks.append(check)

    def run(self) -> ValidationResult:
        """Execute all registered checks."""

        success = True

        for check in self.checks:
            if not check():
                success = False

        return ValidationResult(success=success)
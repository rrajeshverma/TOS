"""
Startup Validation Report

TOS v1.1.1
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class ValidationStatus(Enum):
    """Validation status."""

    PASS = "PASS"
    WARNING = "WARNING"
    FAIL = "FAIL"


@dataclass(slots=True)
class ValidationIssue:
    """Represents a single validation result."""

    name: str
    status: ValidationStatus = ValidationStatus.PASS
    message: str = ""


@dataclass(slots=True)
class ValidationReport:
    """Collection of startup validation results."""

    issues: list[ValidationIssue] = field(default_factory=list)

    def add(self, issue: ValidationIssue) -> None:
        self.issues.append(issue)

    @property
    def pass_count(self) -> int:
        return sum(
            issue.status == ValidationStatus.PASS
            for issue in self.issues
        )

    @property
    def fail_count(self) -> int:
        return sum(
            issue.status == ValidationStatus.FAIL
            for issue in self.issues
        )

    @property
    def warning_count(self) -> int:
        return sum(
            issue.status == ValidationStatus.WARNING
            for issue in self.issues
        )

    @property
    def success(self) -> bool:
        return self.fail_count == 0

    @property
    def health_score(self) -> int:
        if not self.issues:
            return 100

        passed = self.pass_count
        total = len(self.issues)

        return int((passed / total) * 100)

    def __iter__(self):
        return iter(self.issues)

    def __len__(self):
        return len(self.issues)
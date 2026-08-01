"""
Deployment validator.
"""

from __future__ import annotations

import os
import sys


class DeploymentValidator:
    """Validates production deployment prerequisites."""

    def python_version_ok(self) -> bool:
        return sys.version_info >= (3, 12)

    def virtual_environment_active(self) -> bool:
        return sys.prefix != getattr(sys, "base_prefix", sys.prefix)

    def working_directory_exists(self) -> bool:
        return os.path.isdir(os.getcwd())

    def validation_summary(self) -> dict[str, bool]:
        return {
            "python": self.python_version_ok(),
            "venv": self.virtual_environment_active(),
            "cwd": self.working_directory_exists(),
        }

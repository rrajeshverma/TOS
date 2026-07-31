from __future__ import annotations

import subprocess
import sys


def run_tos(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "tos.py", *args],
        capture_output=True,
        text=True,
    )


def test_version_command():
    result = run_tos("version")

    assert result.returncode == 0


def test_health_command():
    result = run_tos("health")

    assert result.returncode == 0


def test_validate_command():
    result = run_tos("validate")

    assert result.returncode == 0


def test_unknown_command():
    result = run_tos("something_invalid")

    assert result.returncode != 0

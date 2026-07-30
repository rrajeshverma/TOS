from unittest.mock import MagicMock

import pytest

from trading.execution_mode import ExecutionMode
from trading.execution_mode_controller import ExecutionModeController


def test_stores_execution_mode():
    controller = ExecutionModeController(ExecutionMode.PAPER)

    assert controller.mode == ExecutionMode.PAPER


def test_selects_paper_runner():
    paper_runner = MagicMock()
    live_runtime = MagicMock()

    controller = ExecutionModeController(
        ExecutionMode.PAPER,
        paper_runner=paper_runner,
        live_runtime=live_runtime,
    )

    assert controller.runtime is paper_runner


def test_selects_live_runtime():
    paper_runner = MagicMock()
    live_runtime = MagicMock()

    controller = ExecutionModeController(
        ExecutionMode.LIVE,
        paper_runner=paper_runner,
        live_runtime=live_runtime,
    )

    assert controller.runtime is live_runtime


def test_invalid_mode_raises():
    with pytest.raises(ValueError):
        ExecutionModeController("INVALID")

def test_start_calls_paper_runner():
    paper_runner = MagicMock()
    live_runtime = MagicMock()

    controller = ExecutionModeController(
        ExecutionMode.PAPER,
        paper_runner=paper_runner,
        live_runtime=live_runtime,
    )

    controller.start()

    paper_runner.start.assert_called_once_with()


def test_start_calls_live_runtime():
    paper_runner = MagicMock()
    live_runtime = MagicMock()

    controller = ExecutionModeController(
        ExecutionMode.LIVE,
        paper_runner=paper_runner,
        live_runtime=live_runtime,
    )

    controller.start()

    live_runtime.start.assert_called_once_with()

# ---------- Stop delegation ----------

def test_stop_calls_paper_runner():
    paper_runner = MagicMock()
    live_runtime = MagicMock()

    controller = ExecutionModeController(
        ExecutionMode.PAPER,
        paper_runner=paper_runner,
        live_runtime=live_runtime,
    )

    controller.stop()

    paper_runner.stop.assert_called_once_with()


def test_stop_calls_live_runtime():
    paper_runner = MagicMock()
    live_runtime = MagicMock()

    controller = ExecutionModeController(
        ExecutionMode.LIVE,
        paper_runner=paper_runner,
        live_runtime=live_runtime,
    )

    controller.stop()

    live_runtime.stop.assert_called_once_with()
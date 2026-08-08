from unittest.mock import Mock, patch

from runtime.launcher import Launcher
from runtime.runtime_mode import RuntimeMode


class DummyRuntime:
    def __init__(self):
        self.started = False

    def start(self):
        self.started = True


def test_launcher_dispatches_version():
    launcher = Launcher()

    assert launcher.run(RuntimeMode.VERSION) == 0


def test_launcher_calls_dispatcher():
    launcher = Launcher()

    launcher._dispatcher = Mock()
    launcher._dispatcher.dispatch.return_value = 0

    launcher.run(RuntimeMode.PAPER)

    launcher._dispatcher.dispatch.assert_called_once_with(
        RuntimeMode.PAPER,
    )


def test_launcher_returns_dispatch_result():
    launcher = Launcher()

    launcher._dispatcher = Mock()
    launcher._dispatcher.dispatch.return_value = 123

    assert launcher.run(RuntimeMode.LIVE) == 123


def test_launcher_creates_dispatcher():
    with patch(
        "runtime.launcher.CommandDispatcher",
    ) as dispatcher:
        Launcher()

        dispatcher.assert_called_once_with()

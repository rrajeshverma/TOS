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

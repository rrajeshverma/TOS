from runtime.dispatcher import CommandDispatcher
from runtime.runtime_mode import RuntimeMode


def test_dispatch_version():
    dispatcher = CommandDispatcher()

    assert dispatcher.dispatch(RuntimeMode.VERSION) == 0


def test_dispatch_health():
    dispatcher = CommandDispatcher()

    assert dispatcher.dispatch(RuntimeMode.HEALTH) == 0


def test_dispatch_validate():
    dispatcher = CommandDispatcher()

    assert dispatcher.dispatch(RuntimeMode.VALIDATE) == 0


def test_paper_registered():
    dispatcher = CommandDispatcher()

    assert RuntimeMode.PAPER in dispatcher._commands


def test_live_registered():
    dispatcher = CommandDispatcher()

    assert RuntimeMode.LIVE in dispatcher._commands

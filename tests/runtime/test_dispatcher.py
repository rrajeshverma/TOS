from unittest.mock import Mock, patch

from runtime.dispatcher import CommandDispatcher
from runtime.runtime_mode import RuntimeMode


@patch("runtime.dispatcher.ConfigValidator")
@patch("runtime.dispatcher.SettingsLoader")
def test_dispatch_validate(
    mock_settings_loader,
    mock_config_validator,
):
    manager = Mock()

    loader = mock_settings_loader.return_value
    loader.load_json.return_value = manager

    validator = mock_config_validator.return_value

    dispatcher = CommandDispatcher()

    assert dispatcher.dispatch(RuntimeMode.VALIDATE) == 0

    loader.load_json.assert_called_once()
    mock_config_validator.assert_called_once_with(manager)
    validator.validate.assert_called_once()

def test_dispatch_version():
    dispatcher = CommandDispatcher()

    assert dispatcher.dispatch(RuntimeMode.VERSION) == 0


def test_dispatch_health():
    dispatcher = CommandDispatcher()

    assert dispatcher.dispatch(RuntimeMode.HEALTH) == 0


def test_paper_registered():
    dispatcher = CommandDispatcher()

    assert RuntimeMode.PAPER in dispatcher._commands


def test_live_registered():
    dispatcher = CommandDispatcher()

    assert RuntimeMode.LIVE in dispatcher._commands

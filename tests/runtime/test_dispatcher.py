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


@patch("builtins.print")
def test_dispatch_unknown_mode(mock_print):
    dispatcher = CommandDispatcher()

    result = dispatcher.dispatch("UNKNOWN")

    assert result == 1

    mock_print.assert_called_once_with(
        "Unsupported mode: UNKNOWN",
    )


@patch("builtins.print")
@patch("runtime.dispatcher.ConfigValidator")
@patch("runtime.dispatcher.SettingsLoader")
def test_dispatch_validate_failure(
    mock_settings_loader,
    mock_config_validator,
    mock_print,
):
    manager = object()

    loader = mock_settings_loader.return_value
    loader.load_json.return_value = manager

    validator = mock_config_validator.return_value
    validator.validate.side_effect = RuntimeError(
        "Invalid configuration",
    )

    dispatcher = CommandDispatcher()

    result = dispatcher.dispatch(RuntimeMode.VALIDATE)

    assert result == 1

    mock_print.assert_called_once_with(
        "Configuration validation failed: Invalid configuration",
    )


@patch("builtins.print")
def test_dispatch_live(
    mock_print,
):
    dispatcher = CommandDispatcher()

    result = dispatcher.dispatch(RuntimeMode.LIVE)

    assert result == 0

    mock_print.assert_called_once_with(
        "Live mode not yet implemented.",
    )


@patch("runtime.dispatcher.application_main")
def test_dispatch_paper(mock_application_main):
    mock_application_main.return_value = 0

    dispatcher = CommandDispatcher()

    result = dispatcher.dispatch(RuntimeMode.PAPER)

    assert result == 0

    mock_application_main.assert_called_once_with()


@patch("runtime.dispatcher.BacktestApplication")
def test_dispatch_backtest(mock_backtest_application):
    mock_backtest_application.return_value.run.return_value = 0

    dispatcher = CommandDispatcher()

    result = dispatcher.dispatch(RuntimeMode.BACKTEST)

    assert result == 0
    mock_backtest_application.return_value.run.assert_called_once_with()

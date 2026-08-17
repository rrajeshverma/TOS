from unittest.mock import MagicMock, patch

import main


@patch("main.TelegramNotifier")
@patch("main.startup")
@patch("main.create_application")
def test_main_starts_runtime(
    mock_create_application,
    mock_startup,
    mock_telegram_notifier,
):
    app = MagicMock()
    app.running = False

    runtime = MagicMock()

    app.services = {
        "trading_runtime": runtime,
    }

    mock_create_application.return_value = app

    main.main()

    runtime.start.assert_called_once()
    mock_telegram_notifier.return_value.send.assert_called_once_with(
        "🟢 TOS STARTED\nMarket: NIFTY\nMode: PAPER"
    )


@patch("main.TelegramNotifier")
def test_graceful_shutdown_sends_telegram(mock_telegram_notifier):
    app = MagicMock()

    notifier = mock_telegram_notifier.return_value

    main.graceful_shutdown(
        app,
        notifier,
    )

    notifier.send.assert_called_once_with("🔴 TOS STOPPED\nTOS shutdown completed.")

    app.shutdown.assert_called_once()

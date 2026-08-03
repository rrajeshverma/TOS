from unittest.mock import MagicMock, patch

import main


@patch("main.startup")
@patch("main.create_application")
def test_main_starts_runtime(
    mock_create_application,
    mock_startup,
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

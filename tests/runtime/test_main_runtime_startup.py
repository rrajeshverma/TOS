from unittest.mock import MagicMock, patch

import main


@patch("main.TradingRuntime")
@patch("main.startup")
@patch("main.create_application")
def test_main_starts_runtime(
    mock_create_application,
    mock_startup,
    mock_runtime,
):
    app = MagicMock()
    app.running = False

    mock_create_application.return_value = app

    runtime = MagicMock()
    mock_runtime.return_value = runtime

    main.main()

    runtime.start.assert_called_once()

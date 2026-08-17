from unittest.mock import MagicMock, patch

from services.telegram_notifier import TelegramNotifier


def test_telegram_disabled_without_credentials(monkeypatch):
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)

    notifier = TelegramNotifier()

    assert notifier.enabled is False
    assert notifier.send("test") is False


@patch("services.telegram_notifier.urllib.request.urlopen")
def test_telegram_send_success(mock_urlopen):
    response = MagicMock()
    response.__enter__.return_value = response
    response.__exit__.return_value = False
    response.read.return_value = b'{"ok": true}'

    mock_urlopen.return_value = response

    notifier = TelegramNotifier(
        bot_token="TOKEN",
        chat_id="CHAT",
    )

    assert notifier.enabled is True
    assert notifier.send("hello") is True

    mock_urlopen.assert_called_once()


@patch("services.telegram_notifier.urllib.request.urlopen")
def test_telegram_failure_does_not_raise(mock_urlopen):
    mock_urlopen.side_effect = RuntimeError("telegram unavailable")

    notifier = TelegramNotifier(
        bot_token="TOKEN",
        chat_id="CHAT",
    )

    assert notifier.send("hello") is False

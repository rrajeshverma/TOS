"""
Telegram notification service.

Notification-only integration. It must never block or control trading.
"""

from __future__ import annotations

import json
import logging
import os
import urllib.parse
import urllib.request

LOGGER = logging.getLogger(__name__)


class TelegramNotifier:
    """Sends notification-only Telegram messages."""

    def __init__(
        self,
        bot_token: str | None = None,
        chat_id: str | None = None,
    ) -> None:
        self.bot_token = bot_token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")

    @property
    def enabled(self) -> bool:
        return bool(self.bot_token and self.chat_id)

    def send(self, message: str) -> bool:
        """Send a Telegram message without affecting trading."""
        if not self.enabled:
            return False

        try:
            payload = urllib.parse.urlencode(
                {
                    "chat_id": self.chat_id,
                    "text": message,
                }
            ).encode()

            request = urllib.request.Request(
                f"https://api.telegram.org/bot{self.bot_token}/sendMessage",
                data=payload,
                method="POST",
            )

            with urllib.request.urlopen(request, timeout=10) as response:
                result = json.load(response)

            if result.get("ok") is not True:
                LOGGER.warning("Telegram notification failed: %s", result)
                return False

            return True

        except Exception:
            LOGGER.exception("Telegram notification error")
            return False

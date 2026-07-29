"""
TOS Configuration Validator

Validates production startup configuration.
"""

from __future__ import annotations


class ConfigValidator:
    """
    Validates required TOS configuration.
    """

    def validate(
        self,
        config: dict,
    ) -> bool:
        """
        Validate configuration.
        """

        if not config:
            return False

        required = [
            "mode",
            "broker",
        ]

        for key in required:
            if key not in config:
                return False

        return True

    def is_live_safe(
        self,
        config: dict,
    ) -> bool:
        """
        Validate LIVE trading safety.
        """

        if config.get("mode") != "LIVE":
            return True

        return bool(
            config.get(
                "live_approved",
                False,
            )
        )

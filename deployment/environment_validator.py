"""
TOS Environment Safety Validator

Validates deployment environment settings.
"""

from __future__ import annotations


class EnvironmentValidator:
    """
    Validates runtime environment.
    """

    REQUIRED_KEYS = (
        "TOS_MODE",
        "BROKER",
    )

    def validate(
        self,
        environment: dict,
    ) -> bool:
        """
        Validate required environment values.
        """

        if not environment:
            return False

        for key in self.REQUIRED_KEYS:
            if not environment.get(key):
                return False

        return True

    def has_credentials(
        self,
        environment: dict,
    ) -> bool:
        """
        Check broker credentials exist.
        """

        return bool(environment.get("ACCESS_TOKEN"))

    def is_production_safe(
        self,
        environment: dict,
    ) -> bool:
        """
        Validate production safety.
        """

        if environment.get("TOS_MODE") != "LIVE":
            return True

        return (
            self.has_credentials(environment)
            and environment.get(
                "LIVE_APPROVED",
                False,
            )
            is True
        )

"""
TOS Runtime Alert Manager

Generates and stores operational alerts.
"""

from __future__ import annotations


class AlertManager:
    """
    Handles runtime alerts.
    """

    def __init__(self) -> None:

        self._alerts: list[dict] = []


    def raise_alert(
        self,
        alert_type: str,
        message: str,
    ) -> dict:
        """
        Create runtime alert.
        """

        alert = {
            "type": alert_type,
            "message": message,
        }

        self._alerts.append(
            alert
        )

        return alert


    def alerts(
        self,
    ) -> list[dict]:
        """
        Return alerts snapshot.
        """

        return list(
            self._alerts
        )


    def count(
        self,
    ) -> int:
        """
        Return alert count.
        """

        return len(
            self._alerts
        )


    def has_alert(
        self,
        alert_type: str,
    ) -> bool:
        """
        Check alert type exists.
        """

        return any(
            alert["type"] == alert_type
            for alert in self._alerts
        )


    def clear(
        self,
    ) -> None:
        """
        Clear alerts.
        """

        self._alerts.clear()

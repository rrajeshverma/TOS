"""
TOS Deployment Smoke Test

Validates complete production deployment flow.
"""

from __future__ import annotations


class DeploymentSmokeTest:
    """
    Runs deployment readiness checks.
    """

    def __init__(self) -> None:

        self._steps: dict[str, bool] = {}


    def register(
        self,
        step: str,
        passed: bool,
    ) -> None:
        """
        Register deployment check.
        """

        self._steps[step] = passed


    def is_successful(
        self,
    ) -> bool:
        """
        Return deployment result.
        """

        if not self._steps:
            return False

        return all(
            self._steps.values()
        )


    def failed_steps(
        self,
    ) -> list[str]:
        """
        Return failed deployment steps.
        """

        return [
            step
            for step, status
            in self._steps.items()
            if not status
        ]


    def reset(
        self,
    ) -> None:
        """
        Reset deployment state.
        """

        self._steps.clear()

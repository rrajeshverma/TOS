"""
Service information for Trading Operating System.
"""

from dataclasses import dataclass

from config.version import APP_NAME, BUILD, MODE, VERSION


@dataclass(frozen=True, slots=True)
class ServiceInfo:
    """Production service metadata."""

    name: str = APP_NAME
    version: str = VERSION
    build: str = BUILD
    mode: str = MODE

    @property
    def display_name(self) -> str:
        """Return formatted service name."""

        return f"{self.name} v{self.version}"

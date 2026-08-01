"""
Systemd service writer.
"""

from __future__ import annotations

from pathlib import Path

from deployment.systemd_service import SystemdService


class SystemdServiceWriter:
    """Writes a systemd service file."""

    def write(
        self,
        service: SystemdService,
        destination: Path,
    ) -> Path:
        """Write the service definition."""

        destination.write_text(
            service.render(),
            encoding="utf-8",
        )

        return destination

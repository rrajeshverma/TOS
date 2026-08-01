"""
systemd service generator.
"""

from dataclasses import dataclass

from deployment.service_info import ServiceInfo


@dataclass(frozen=True, slots=True)
class SystemdService:
    """Represents a systemd service definition."""

    service_info: ServiceInfo

    @property
    def service_name(self) -> str:
        return "tos.service"

    @property
    def description(self) -> str:
        return self.service_info.display_name

    @property
    def restart_policy(self) -> str:
        return "always"

    @property
    def wanted_by(self) -> str:
        return "multi-user.target"

    @property
    def exec_start(self) -> str:
        return "python3 main.py"

    def render(self) -> str:
        """Render a systemd service file."""

        return f"""[Unit]
    Description={self.description}
    After=network.target

    [Service]
    Type=simple
    ExecStart={self.exec_start}
    Restart={self.restart_policy}

    [Install]
    WantedBy={self.wanted_by}
    """

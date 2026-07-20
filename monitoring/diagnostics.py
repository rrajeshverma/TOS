from monitoring.health_check import HealthCheck
from monitoring.runtime_status import RuntimeStatus
from monitoring.system_monitor import SystemMonitor


class Diagnostics:
    def __init__(self):
        self.health = HealthCheck()
        self.runtime = RuntimeStatus()
        self.system = SystemMonitor()

    def report(self):
        return {
            "healthy": self.health.overall_status(),
            "running": self.runtime.is_running,
            "uptime": self.runtime.uptime_seconds(),
            "system": self.system.as_dict(),
            "failed_checks": self.health.failed_checks(),
        }

    def __repr__(self):
        return (
            f"Diagnostics("
            f"healthy={self.health.overall_status()}, "
            f"running={self.runtime.is_running})"
        )

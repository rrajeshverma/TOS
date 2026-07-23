import os
import platform
import sys


class SystemMonitor:
    @property
    def python_version(self):
        return sys.version.split()[0]

    @property
    def platform(self):
        return platform.system()

    @property
    def platform_release(self):
        return platform.release()

    @property
    def cpu_count(self):
        return os.cpu_count() or 1

    @property
    def process_id(self):
        return os.getpid()

    def as_dict(self):
        return {
            "python_version": self.python_version,
            "platform": self.platform,
            "platform_release": self.platform_release,
            "cpu_count": self.cpu_count,
            "process_id": self.process_id,
        }

    def __repr__(self):
        return f"SystemMonitor(platform={self.platform}, python={self.python_version})"

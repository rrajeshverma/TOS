from dataclasses import dataclass


@dataclass
class KillSwitch:
    enabled: bool = False

    def activate(self):
        self.enabled = True

    def deactivate(self):
        self.enabled = False

    def is_enabled(self):
        return self.enabled
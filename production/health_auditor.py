class HealthAuditor:
    """
    Monitors component health.
    """

    def __init__(self):
        self.health = {}

    def register(self, name):
        self.health[name] = True

    def has_component(self, name):
        return name in self.health

    def mark_failed(self, name):
        if name in self.health:
            self.health[name] = False

    def is_healthy(self):
        return all(self.health.values()) if self.health else False

    def report(self):
        return {
            "health": self.health.copy()
        }
class FailoverValidator:
    """
    Tracks service availability and failover state.
    """

    def __init__(self):
        self.services = {}

    def register(self, name):
        self.services[name] = True

    def has_service(self, name):
        return name in self.services

    def validate(self, name):
        return self.services.get(name, False)

    def fail(self, name):
        if name in self.services:
            self.services[name] = False

    def summary(self):
        return {"services": self.services.copy()}

class HealthCheck:
    def __init__(self):
        self._checks = {}

    def register(self, name, status=True):
        self._checks[name] = bool(status)

    def update(self, name, status):
        self._checks[name] = bool(status)

    def status(self, name):
        return self._checks.get(name)

    def overall_status(self):
        return all(self._checks.values()) if self._checks else True

    def count(self):
        return len(self._checks)

    def failed_checks(self):
        return [name for name, status in self._checks.items() if not status]

    def clear(self):
        self._checks.clear()

    def __len__(self):
        return len(self._checks)

    def __repr__(self):
        return (
            f"HealthCheck(" f"checks={len(self)}, " f"healthy={self.overall_status()})"
        )

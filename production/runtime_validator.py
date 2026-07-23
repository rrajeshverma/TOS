class RuntimeValidator:
    """
    Validates runtime configuration.
    """

    def __init__(self):
        self.runtime = {}

    def set(self, key, value):
        self.runtime[key] = value

    def get(self, key, default=None):
        return self.runtime.get(key, default)

    def validate(self):
        return len(self.runtime) > 0

    def summary(self):
        return {"runtime": self.runtime.copy()}

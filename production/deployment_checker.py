class DeploymentChecker:
    """
    Validates deployment readiness.
    """

    def __init__(self):
        self.components = set()

    def add_component(self, name):
        self.components.add(name)

    def has_component(self, name):
        return name in self.components

    def is_ready(self):
        return len(self.components) > 0

    def summary(self):
        return {
            "components": list(self.components),
            "ready": self.is_ready(),
        }
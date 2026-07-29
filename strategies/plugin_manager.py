"""
Plugin manager for strategy plugins.
"""


class PluginManager:
    """Manages strategy plugin instances."""

    def __init__(self) -> None:
        self.plugins: list[object] = []

    def register(self, plugin: object) -> None:
        """Register a plugin."""

        if plugin is None:
            raise ValueError("Plugin cannot be None")

        self.plugins.append(plugin)

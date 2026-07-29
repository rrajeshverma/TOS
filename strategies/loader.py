"""
Strategy loader.
"""

from __future__ import annotations

import pkgutil

import strategies.plugins


class StrategyLoader:
    """Maintains a collection of strategy plugins."""

    def __init__(self) -> None:
        self.plugins: list[object] = []

    def add(self, plugin: object) -> None:
        """Add a plugin."""

        if plugin is None:
            raise ValueError("Plugin cannot be None")

        self.plugins.append(plugin)

    def discover(self) -> list[str]:
        """
        Discover available strategy plugin modules.
        """

        return sorted(
            module.name
            for module in pkgutil.iter_modules(strategies.plugins.__path__)
            if not module.name.startswith("_")
        )
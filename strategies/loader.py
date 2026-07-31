"""
Strategy loader.
"""

from __future__ import annotations

import importlib
import pkgutil

import strategies.plugins

import inspect

from strategies.base_strategy import BaseStrategy


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

    def load(self) -> list[object]:
        """
        Import all discovered strategy plugin modules.
        """

        return [
            importlib.import_module(f"strategies.plugins.{name}")
            for name in self.discover()
        ]

    def strategy_classes(self) -> list[type[BaseStrategy]]:
        """
        Discover all BaseStrategy subclasses from loaded plugin modules.
        """

        classes: list[type[BaseStrategy]] = []

        for module in self.load():
            for _, cls in inspect.getmembers(module, inspect.isclass):
                if (
                    issubclass(cls, BaseStrategy)
                    and cls is not BaseStrategy
                    and cls.__module__ == module.__name__
                ):
                    classes.append(cls)

        return classes

    def instances(self) -> list[BaseStrategy]:
        """
        Instantiate all discovered strategy classes.
        """

        return [strategy_class() for strategy_class in self.strategy_classes()]

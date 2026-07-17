from collections import OrderedDict
from itertools import product


class ParameterSpace:
    def __init__(self):
        self._parameters = OrderedDict()

    @property
    def parameters(self):
        return dict(self._parameters)

    def add(self, name, values):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Parameter name must be a non-empty string.")

        if name in self._parameters:
            raise ValueError(f"Parameter '{name}' already exists.")

        values = list(values)

        if not values:
            raise ValueError("Parameter values cannot be empty.")

        self._parameters[name] = values

    def remove(self, name):
        self._parameters.pop(name, None)

    def clear(self):
        self._parameters.clear()

    def count(self):
        if not self._parameters:
            return 0

        total = 1
        for values in self._parameters.values():
            total *= len(values)
        return total

    def generate(self):
        if not self._parameters:
            return iter(())

        names = list(self._parameters.keys())
        values = list(self._parameters.values())

        return (
            dict(zip(names, combo))
            for combo in product(*values)
        )

    def __len__(self):
        return len(self._parameters)

    def __contains__(self, item):
        return item in self._parameters

    def __iter__(self):
        return iter(self._parameters.items())
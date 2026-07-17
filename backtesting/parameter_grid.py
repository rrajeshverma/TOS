from itertools import product


class ParameterGrid:
    def __init__(self, parameters):
        self.parameters = parameters

    def generate(self):
        keys = list(self.parameters.keys())
        values = [self.parameters[key] for key in keys]

        for combination in product(*values):
            yield dict(zip(keys, combination))
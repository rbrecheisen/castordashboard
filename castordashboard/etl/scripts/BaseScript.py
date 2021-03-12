from types import SimpleNamespace


class BaseScript:

    def __init__(self, name, runner, params):
        self.name = name
        self.runner = runner
        self.params = params
        if isinstance(self.params, dict):
            self.params = SimpleNamespace(**params)

    def execute(self):
        raise NotImplementedError()

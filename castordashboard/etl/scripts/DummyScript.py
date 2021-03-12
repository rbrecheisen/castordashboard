from . import BaseScript


class DummyScript(BaseScript):

    def __init__(self, runner, params):
        super(DummyScript, self).__init__(self.__class__, runner, params)

    def execute(self):
        self.runner.logger.print(json.dumps(vars(self.params), indent=4))

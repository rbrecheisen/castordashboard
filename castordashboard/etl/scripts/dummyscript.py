from . import BaseScript


class DummyScript(BaseScript):

    def __init__(self, name, runner, params):
        super(DummyScript, self).__init__(name, runner, params)

    def execute(self, output_dir):
        self.save_to_json(self.params, output_dir)

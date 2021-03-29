from . import BaseScript


class DummyScript(BaseScript):

    def __init__(self, name, logger, params):
        super(DummyScript, self).__init__(name, logger, params)

    def execute(self):
        self.save_to_json(self.params, self.params['output_dir'])

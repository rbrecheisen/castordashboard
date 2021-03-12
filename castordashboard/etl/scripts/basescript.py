import os
import json


class BaseScript:

    def __init__(self, name, runner, params):
        self.name = name
        self.runner = runner
        self.params = params
        self.script_params = params['scripts'][name]

    def save_to_json(self, data, output_dir):
        with open(os.path.join(output_dir, self.name + '.json'), 'w') as f:
            json.dump(data, f, indent=4)

    def execute(self, output_dir):
        raise NotImplementedError()

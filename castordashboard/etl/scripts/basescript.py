import os
import json


class BaseScript:

    def __init__(self, name, logger, params):
        self.name = name
        self.logger = logger
        self.params = params

    def save_to_json(self, data, output_dir):
        with open(os.path.join(output_dir, self.name + '.json'), 'w') as f:
            json.dump(data, f, indent=4)

    def execute(self):
        raise NotImplementedError()

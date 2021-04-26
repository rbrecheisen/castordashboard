import os
import json


class BaseScript:

    def __init__(self, name, logger):
        self.name = name
        self.logger = logger

    def save_to_json(self, data, output_dir):

        # Save script output to JSON. Do not write finished.txt file here because there may
        # be other scripts following. We want the whole script runner to finish before we
        # write finished.txt
        with open(os.path.join(output_dir, self.name + '.json'), 'w') as f:
            json.dump(data, f, indent=4)

    def execute(self):
        raise NotImplementedError()

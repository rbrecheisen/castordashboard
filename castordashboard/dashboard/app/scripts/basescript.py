import os
import json

from django.conf import settings


class BaseScript:

    def __init__(self, name):
        self.name = name
        self.timestamp = None
        self.params = self.load_params()

    @staticmethod
    def load_params():
        with open(settings.PARAMS_FILE_PATH, 'r') as f:
            return json.load(f)

    def find_most_recent_data_dir(self):
        ld = None
        max_x = 0
        for d in os.listdir(self.params['output_dir']):
            try:
                x = int(d)
                d = os.path.join(self.params['output_dir'], d)
                if os.path.isfile(os.path.join(d, 'finished.txt')) and x > max_x:
                    ld = d
                    max_x = x
            except ValueError:
                pass
        print('Latest (finished) directory: {}'.format(ld))
        return ld

    def load_data(self):
        data_dir = self.find_most_recent_data_dir()
        if data_dir is not None:
            with open(os.path.join(data_dir, '{}.json'.format(self.name)), 'r') as f:
                self.timestamp = data_dir.split(os.path.sep)[-1]
                return json.load(f)
        return None

    def get_plots(self):
        raise NotImplementedError()

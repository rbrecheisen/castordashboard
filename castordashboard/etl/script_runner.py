import os
import json
import argparse
import importlib
import datetime

from barbell2.utils import Logger, current_time_secs, elapsed_secs


class ScriptRunner:

    def __init__(self, params):
        self.params = params
        self.scripts = []
        self.logger = Logger(prefix='log_etl')

    def get_output_dir(self):
        os.makedirs(self.params['output_dir'], exist_ok=True)
        now = datetime.datetime.now()
        timestamp = '{}'.format(now.strftime('%Y%m%d%H%M%S'))
        os.makedirs(os.path.join(self.params['output_dir'], timestamp), exist_ok=True)
        output_dir = os.path.join(self.params['output_dir'], timestamp)
        return output_dir

    def execute(self):
        if len(self.scripts) == 0:
            self.logger.print('Nothing to execute')
            return
        output_dir = self.get_output_dir()
        start_overall = current_time_secs()
        for script in self.scripts:
            self.logger.print('Starting script {}'.format(script.name))
            start = current_time_secs()
            script.execute(output_dir)
            self.logger.print(
                'Script finished after {} seconds'.format(elapsed_secs(start)))
        self.logger.print(
            'Elapsed overall: {} seconds'.format(elapsed_secs(start_overall)))


def main():

    if not os.path.isfile('params.json'):
        raise RuntimeError('Missing params.json file!')
    with open('params.json', 'r') as f:
        params = json.load(f)

    runner = ScriptRunner(params)
    for script_name in params['scripts'].keys():
        script = getattr(importlib.import_module('castordashboard.etl.scripts'), script_name)
        runner.scripts.append(script(script_name, runner, params))
    runner.execute()


if __name__ == '__main__':
    main()

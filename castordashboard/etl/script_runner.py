import os
import json
import importlib
import datetime

from barbell2light.utils import Logger, current_time_secs, elapsed_secs


class ScriptRunner:

    def __init__(self, params):
        self.params = params
        self.params['output_dir'] = self.update_output_dir()
        os.makedirs(params['log_dir'], exist_ok=True)
        self.logger = Logger(prefix='log_etl', to_dir=params['log_dir'])
        self.scripts = self.load_scripts(self.logger, self.params)

    def update_output_dir(self):

        # Append timestamp to configured output directory
        os.makedirs(self.params['output_dir'], exist_ok=True)
        now = datetime.datetime.now()
        timestamp = '{}'.format(now.strftime('%Y%m%d%H%M%S'))
        os.makedirs(os.path.join(self.params['output_dir'], timestamp), exist_ok=True)
        output_dir = os.path.join(self.params['output_dir'], timestamp)
        return output_dir

    @staticmethod
    def load_scripts(logger, params):

        # Load script instances configured in the parameter file
        scripts_package = os.environ.get('SCRIPTS_PACKAGE', 'etl.scripts')
        scripts = []
        if 'scripts' in params.keys():
            for script_name in params['scripts']:
                m = importlib.import_module('{}.{}'.format(scripts_package, script_name.lower()))
                script = getattr(m, script_name)
                scripts.append(script(script_name, logger, params))
        return scripts

    def execute(self):

        # If there are no scripts, return immediately
        if len(self.scripts) == 0:
            self.logger.print('Nothing to execute')
            return

        # Start iterating over the separate scripts and keep track of the time
        start_overall = current_time_secs()
        for script in self.scripts:
            self.logger.print('Starting script {}'.format(script.name))
            start = current_time_secs()
            script.execute()
            self.logger.print(
                'Script finished after {} seconds'.format(elapsed_secs(start)))
        self.logger.print(
            'Elapsed overall: {} seconds'.format(elapsed_secs(start_overall)))

        # Write finished.txt file to output directory so the dashboard application
        # knows which output directory contains the latest data
        os.system('touch {}'.format(
            os.path.join(self.params['output_dir'], 'finished.txt')))


def main():
    with open(os.environ.get('PARAMS_FILE_PATH', 'params.json'), 'r') as f:
        params = json.load(f)
    runner = ScriptRunner(params)
    runner.execute()


if __name__ == '__main__':
    main()

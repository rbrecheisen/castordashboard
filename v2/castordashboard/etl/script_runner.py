import os
import importlib
import datetime
from .scripts import RetrieveProcedureComplicationsPerQuarterScript


from barbell2light.utils import Logger, current_time_secs, elapsed_secs


class ScriptRunner:

    def __init__(self):
        self.output_dir = os.environ['CASTOR_DASHBOARD_ETL_OUTPUT']
        self.output_dir = self.update_output_dir(self.output_dir)
        log_dir = os.environ['CASTOR_DASHBOARD_ETL_LOG_DIR']
        os.makedirs(log_dir, exist_ok=True)
        self.logger = Logger(prefix='log_etl', to_dir=log_dir)
        script_names = [x.strip() for x in os.environ['CASTOR_DASHBOARD_SCRIPT_NAMES'].split(',')]
        self.scripts = self.load_scripts(self.logger, script_names)

    @staticmethod
    def update_output_dir(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        now = datetime.datetime.now()
        timestamp = '{}'.format(now.strftime('%Y%m%d%H%M%S'))
        os.makedirs(os.path.join(output_dir, timestamp), exist_ok=True)
        output_dir = os.path.join(output_dir, timestamp)
        return output_dir

    @staticmethod
    def load_scripts(logger, script_names):
        scripts_package = os.environ['CASTOR_DASHBOARD_SCRIPTS_PACKAGE']
        scripts = []
        for script_name in script_names:
            m = importlib.import_module('{}.{}'.format(scripts_package, script_name.lower()))
            script = getattr(m, script_name)
            scripts.append(script(script_name, logger))
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
            os.path.join(self.output_dir, 'finished.txt')))


def main():
    runner = ScriptRunner()
    runner.execute()


if __name__ == '__main__':
    main()

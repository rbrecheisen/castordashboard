import os
import datetime
from .scripts import RetrieveProcedureComplicationsPerQuarterScript
from barbell2light.utils import Logger, current_time_secs, elapsed_secs


class ScriptRunner:

    def __int__(self, output_dir, log_dir):
        self.output_dir = output_dir
        self.output_dir = self.update_output_dir(self.output_dir)
        log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.logger = Logger(prefix='log_etl', to_dir=log_dir)
        self.scripts = [
            RetrieveProcedureComplicationsPerQuarterScript(self.logger, self.output_dir),
        ]

    @staticmethod
    def update_output_dir(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        now = datetime.datetime.now()
        timestamp = '{}'.format(now.strftime('%Y%m%d%H%M%S'))
        os.makedirs(os.path.join(output_dir, timestamp), exist_ok=True)
        output_dir = os.path.join(output_dir, timestamp)
        return output_dir

    def execute(self):
        runner_started = current_time_secs()
        for s in self.scripts:
            self.logger.print('Starting script {}'.format(s.name))
            script_started = current_time_secs()
            s.execute()
            self.logger.print('Script finished after {}'.format(elapsed_secs(script_started)))
        self.logger.print('Runner finished after {}'.format(elapsed_secs(runner_started)))
        os.system('touch {}'.format(
            os.path.join(self.output_dir, 'finished.txt')))


def main():
    # output_dir = os.environ['CASTOR_DASHBOARD_ETL_OUTPUT']
    # log_dir = os.environ['CASTOR_DASHBOARD_ETL_LOG_DIR']
    # runner = ScriptRunner(output_dir, log_dir)
    # runner.execute()
    pass


if __name__ == '__main__':
    main()

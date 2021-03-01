import time
import argparse

from types import SimpleNamespace
from barbell2.utils import Logger, current_time_secs, elapsed_secs


class ScriptRunner:

    def __init__(self, interval=0, time_period=0):
        self.interval = interval
        self.time_period = self.get_time_period_in_secs(time_period)
        self.script = None
        self.logger = Logger(prefix='log_etl')

    @staticmethod
    def get_time_period_in_secs(time_period):
        if isinstance(time_period, int):
            return time_period
        if isinstance(time_period, str):
            if time_period == 'minute':
                return 60
            if time_period == 'hour':
                return 3600
            if time_period == 'day':
                return 24 * 3600
            if time_period == 'week':
                return 7 * 24 * 3600
            if time_period == 'month':
                return 30 * 7 * 24 * 3600
            if time_period == 'year':
                return 12 * 30 * 7 * 24 * 3600
        return -1

    def execute(self):

        if self.script is None:
            self.logger.print('Nothing to execute')
            return

        start_time = current_time_secs()
        self.logger.print('Starting runner')

        while True:
            self.logger.print('Executing script {}'.format(self.script.name))
            self.script.execute()
            self.logger.print('Waiting for {} seconds'.format(self.interval))
            time.sleep(self.interval)
            elapsed = elapsed_secs(start_time)
            if elapsed >= self.time_period:
                self.logger.print('Time elapsed > requested period of {} seconds'.format(self.time_period))
                break
        self.logger.print('Runner stopped')


PARAM_HELP = """
Missing argument --params=<Path to JSON parameter file>

For example:

{
    "script":       "RetrieveHistogramWithProcedureCountsScript",
    "study_name":   "ESPRESSO_v2.0_DPCA",
    "year_begin":   2014,
    "year_end":     2018,
    "output_dir":   "/tmp/castordashboard",
    "output_json":  "histogram_dpca.json",
    "use_cache":    false,
    "verbose":      false
}
"""


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--params',
                        help='Full path to JSON parameter file (default: params.json)',
                        default='params.json')
    args = parser.parse_args()

    if args.params is None:
        print(PARAM_HELP)
        return

    import json
    with open(args.params, 'r') as f:
        params = json.load(f)
    params = SimpleNamespace(**params)

    import importlib
    script = getattr(importlib.import_module('castordashboard.etl.scripts'), name=params.script)

    runner = ScriptRunner()
    runner.script = script(runner, params)
    runner.execute()


if __name__ == '__main__':
    main()

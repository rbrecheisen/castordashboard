import time
import json
import argparse
import importlib

from types import SimpleNamespace
from barbell2.utils import Logger, current_time_secs, elapsed_secs


class ScriptRunner:

    def __init__(self, interval=0, time_period=0):
        self.interval = interval
        self.time_period = self.get_time_period_in_secs(time_period)
        self.script = None
        self.logger = Logger(prefix='log_etl')

    def check_params(self):
        pass

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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--params',
                        help='Full path to JSON parameter file (default: params.json)',
                        default='params.json')
    parser.add_argument('--interval',
                        help='Interval (secs) to wait before running script again (default: 0)',
                        default=0)
    parser.add_argument('--time_period',
                        help='Time period (secs) to let script running (default: 0)',
                        default=0)
    parser.add_argument('--script_module',
                        help='Path to Python module containing scripts',
                        default='castordashboard.etl.scripts')
    args = parser.parse_args()
    with open(args.params, 'r') as f:
        params = json.load(f)
    params = SimpleNamespace(**params)
    script = getattr(importlib.import_module(params.script_module), params.script)
    runner = ScriptRunner(params.interval, params.time_period)
    runner.script = script(runner, params)
    runner.execute()


if __name__ == '__main__':
    main()

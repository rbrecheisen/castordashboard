from types import SimpleNamespace
from barbell2.utils import Logger, current_time_secs, elapsed_secs


class ScriptRunner:
    """
    ScriptRunner is able to run one or more scripts that extract data from Castor, transform it
    and save it to file for display at a later point in time. ScriptRunner connects to Castor
    and shares the connection session with each script.
    """
    def __init__(self, params):
        self.params = SimpleNamespace(**params)
        self.interval = self.params.interval
        self.time_period = self.get_time_period_in_secs(self.params.time_period)
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


class Script:
    pass


def main():
    params = {
        'interval': 0,
        'time_period': 0,
    }
    runner = ScriptRunner(params=params)
    runner.execute()


if __name__ == '__main__':
    main()

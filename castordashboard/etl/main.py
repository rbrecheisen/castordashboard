import time
import datetime
from types import SimpleNamespace

from barbell2.utils import Logger, current_time_secs, elapsed_secs


class Runner:

    def __init__(self, params):
        self.params = SimpleNamespace(**params)
        self.script = None
        self.logger = Logger(prefix='cd_etl_Runner')

    def execute(self):

        if self.script is None:
            self.logger.print('Nothing to execute')
            return

        start_time = current_time_secs()
        self.logger.print('Starting runner...')

        while True:
            self.logger.print('Executing script {}...'.format(self.script.name))
            self.script.execute()
            self.logger.print('Waiting for {} seconds...'.format(self.params.interval))
            time.sleep(self.params.interval)
            elapsed = elapsed_secs(start_time)
            if elapsed > self.params.time_period:
                self.logger.print('Time elapsed > requested period of {} seconds'.format(self.params.time_period))
                self.logger.print('Stopping runner execution...')
                break


class Script:

    def __init__(self, name):
        self.name = name

    def execute(self):
        raise NotImplementedError()


class DummyScript(Script):

    def __init__(self):
        super(DummyScript, self).__init__('dummy')

    def execute(self):
        message = 'hello, world!'
        print(message)

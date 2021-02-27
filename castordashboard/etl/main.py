import time

from types import SimpleNamespace
from barbell2.castorclient import CastorClient
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
        self.logger.print('Starting runner')

        while True:
            self.logger.print('Executing script {}'.format(self.script.name))
            self.script.execute()
            self.logger.print('Waiting for {} seconds'.format(self.params.interval))
            time.sleep(self.params.interval)
            elapsed = elapsed_secs(start_time)
            if elapsed >= self.params.time_period:
                self.logger.print('Time elapsed > requested period of {} seconds'.format(self.params.time_period))
                break
        self.logger.print('Runner stopped')


class Script:

    def __init__(self, name, runner):
        self.name = name
        self.runner = runner

    def execute(self):
        raise NotImplementedError()


class DummyScript(Script):

    def __init__(self, runner):
        super(DummyScript, self).__init__(self.__class__, runner)

    def execute(self):
        self.runner.logger.print('hello, world!')


class RetrieveStudyListScript(Script):

    def __init__(self, runner):
        super(RetrieveStudyListScript, self).__init__(self.__class__, runner)

    def execute(self):
        client = CastorClient()
        study_list = client.get_studies()
        for study in study_list:
            self.runner.logger.print(study)


class RetrieveDashboardDataScript(Script):

    def __init__(self, runner):
        super(RetrieveDashboardDataScript, self).__init__(self.__class__, runner)

    def execute(self):
        pass

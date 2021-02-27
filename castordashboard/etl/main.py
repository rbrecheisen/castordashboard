import os
import json
import time

from types import SimpleNamespace
from barbell2.castorclient import CastorClient
from barbell2.utils import Logger, current_time_secs, elapsed_secs


class Runner:

    def __init__(self, interval=0, time_period=0):
        self.interval = interval
        self.time_period = time_period
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
            self.logger.print('Waiting for {} seconds'.format(self.interval))
            time.sleep(self.interval)
            elapsed = elapsed_secs(start_time)
            if elapsed >= self.time_period:
                self.logger.print('Time elapsed > requested period of {} seconds'.format(self.time_period))
                break
        self.logger.print('Runner stopped')


class Script:

    def __init__(self, name, runner, params):
        self.name = name
        self.runner = runner
        self.params = params
        if isinstance(self.params, dict):
            self.params = SimpleNamespace(**params)

    def execute(self):
        raise NotImplementedError()


class DummyScript(Script):

    def __init__(self, runner, params):
        super(DummyScript, self).__init__(self.__class__, runner, params)

    def execute(self):
        self.runner.logger.print('Hello, world!')


class RetrieveStudyListScript(Script):

    def __init__(self, runner, params):
        super(RetrieveStudyListScript, self).__init__(self.__class__, runner, params)

    def execute(self):
        client = CastorClient()
        study_list = client.get_studies()
        for study in study_list:
            self.runner.logger.print(study)


class RetrieveDashboardDataScript(Script):

    def __init__(self, runner, params):
        super(RetrieveDashboardDataScript, self).__init__(self.__class__, runner, params)

    def get_surgery_dates(self):
        pass

    def execute(self):
        # - Get study ID for 'study_name' param
        # - Get fields
        # - Get field ID for 'fields' param
        # - Get records
        # - For each record in records
        #       Get field data
        client = CastorClient()

        study_id = client.get_study_id(self.params.study_name)

        fields = client.get_fields(study_id)
        field_names = self.params.field_names

        field_ids = []
        for field_name in field_names:
            field_ids.append(client.get_field_id(field_name, fields))

        records = client.get_records(study_id)

        field_data = {}
        for i in range(len(field_ids)):
            field_data[field_names[i]] = []
            for record in records:
                data = client.get_field_data(study_id, record['id'], field_ids[i])
                field_data[field_names[i]].append(data)
                self.runner.logger.print(record['id'])
        print(json.dumps(field_data, indent=4))

        # os.makedirs(self.params.output_dir, exist_ok=True)
        # with open(os.path.join(self.params.output_dir, self.params.output_json), 'w') as f:
        #     f.write('bla')

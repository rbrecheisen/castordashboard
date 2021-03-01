import os
import json
import time

from types import SimpleNamespace
from barbell2.castorclient import CastorClient
from barbell2.utils import Logger, current_time_secs, elapsed_secs


class Runner:

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

    @staticmethod
    def get_numerical_representation(date_str):
        items = date_str.split('-')
        return int('{}{}{}'.format(items[2], items[1], items[0]))

    def get_earliest_and_latest_date(self, date_list):
        min_date = 999999999
        min_date_str = ''
        max_date = 0
        max_date_str = ''
        for d in date_list:
            x = self.get_numerical_representation(d)
            if x < min_date:
                min_date = x
                min_date_str = d
            if x > max_date:
                max_date = x
                max_date_str = d
        return min_date_str, max_date_str

    @staticmethod
    def get_year(date_str):
        return int(date_str.split('-')[2])

    @staticmethod
    def get_month(date_str):
        return int(date_str.split('-')[1])

    def get_histogram(self, year_begin, year_end, dates):
        histogram = {}
        for year in range(year_begin, year_end + 1):
            histogram[year] = {
                '1_2_3': 0,
                '4_5_6': 0,
                '7_8_9': 0,
                '10_11_12': 0,
            }
        for d in dates:
            y = self.get_year(d)
            m = str(self.get_month(d))
            if y in histogram.keys():
                for q in histogram[y].keys():
                    x = q.split('_')
                    if m in x:
                        histogram[y][q] += 1
        return histogram

    @staticmethod
    def get_quarter(k):
        if k == '1_2_3':
            return 'q1'
        if k == '4_5_6':
            return 'q2'
        if k == '7_8_9':
            return 'q3'
        return 'q4'

    def flatten_histogram(self, histogram):
        histogram_new = {}
        for y in histogram.keys():
            for k in histogram[y].keys():
                q = self.get_quarter(k)
                histogram_new['{}_{}'.format(y, q)] = histogram[y][k]
        return histogram_new

    def get_surgery_dates(self):
        try:
            use_cache = self.params.use_cache
        except AttributeError:
            use_cache = True
        try:
            verbose = self.params.verbose
        except AttributeError:
            verbose = False
        client = CastorClient()
        study_id = client.get_study_id(self.params.study_name)
        fields = client.get_fields(study_id, use_cache=use_cache, verbose=verbose)
        surgery_date_field_name = self.params.field_name
        surgery_date_field_id = client.get_field_id(surgery_date_field_name, fields)
        records = client.get_records(study_id, use_cache=use_cache, verbose=verbose)
        surgery_dates = []
        for record in records:
            data = client.get_field_data(study_id, record['id'], surgery_date_field_id)
            if 'value' in data.keys():
                # Check this because empty fields return a server error (data point not found)
                surgery_dates.append(data['value'])
                self.runner.logger.print(record['id'])
        return surgery_dates

    def save_histogram(self, histogram):
        os.makedirs(self.params.output_dir, exist_ok=True)
        with open(os.path.join(self.params.output_dir, self.params.output_json), 'w') as f:
            json.dump(histogram, f)

    def execute(self):
        surgery_dates = self.get_surgery_dates()
        earliest_date, latest_date = self.get_earliest_and_latest_date(surgery_dates)
        earliest_year, latest_year = self.get_year(earliest_date), self.get_year(latest_date)
        try:
            year_begin = self.params.year_begin
        except AttributeError:
            year_begin = earliest_year
        try:
            year_end = self.params.year_end
        except AttributeError:
            year_end = latest_year
        histogram = self.get_histogram(year_begin, year_end, surgery_dates)
        histogram = self.flatten_histogram(histogram)
        self.save_histogram(histogram)

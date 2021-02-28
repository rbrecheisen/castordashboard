import os
import json

from types import SimpleNamespace

from castordashboard.etl import Runner
from castordashboard.etl import DummyScript
from castordashboard.etl import RetrieveStudyListScript
from castordashboard.etl import RetrieveDashboardDataScript


def find_latest_log(prefix):
    log_file = None
    max_x = 0
    for f in os.listdir('.'):
        if f.startswith(prefix):
            x = int(f.split('_')[3][:-4])
            if x > max_x:
                max_x = x
                log_file = f
    print('Latest log file: {}'.format(log_file))
    return log_file


def test_periodic_execution():

    runner = Runner(interval=1, time_period=5)
    runner.script = DummyScript(runner, {})
    runner.execute()
    runner.logger.close()

    log_file = find_latest_log('cd_etl_Runner')
    with open(log_file, 'r') as f:
        assert len(f.readlines()) == 18


# def test_retrieve_study_list_every_5_secs():
#
#     runner = Runner(interval=5, time_period=10)
#     runner.script = RetrieveStudyListScript(runner, {})
#     runner.execute()
#     runner.logger.close()
#
#     log_file = find_latest_log('cd_etl_Runner')
#
#     count = 0
#     with open(log_file, 'r') as f:
#         for line in f.readlines():
#             if 'study_id' in line.strip():
#                 count += 1
#     assert count > 0
#
#
# def test_retrieve_dashboard_data():
#
#     params = {
#         'study_name': 'ESPRESSO_v2.0_DHBA',
#         'year_begin': 2014,
#         'year_end': 2018,
#         'field_names': [
#             'dhba_datok',
#         ],
#         'output_dir': '/tmp/castordashboard',
#         'output_json': 'histogram.json',
#     }
#
#     runner = Runner(interval=0, time_period=0)
#     runner.script = RetrieveDashboardDataScript(runner, params)
#     runner.execute()
#     runner.logger.close()
#
#     # params = SimpleNamespace(**params)
#     # with open(os.path.join(params.output_dir, params.output_json), 'r') as f:
#     #     histogram = json.load(f)
#     # for year in range(params.year_begin, params.year_end+1):
#     #     for quarter in ['q1', 'q2', 'q3', 'q4']:
#     #         key = '{}_{}'.format(year, quarter)
#     #         assert key in histogram.keys()

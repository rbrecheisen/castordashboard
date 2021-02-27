import os

from castordashboard.etl import Runner, DummyScript, RetrieveStudyListScript, RetrieveDashboardDataScript


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


def test_params():

    runner = Runner(params={'name': 'value'})
    print(runner.params.name)


def test_periodic_execution():

    runner = Runner(params={'interval': 1, 'time_period': 5})
    runner.script = DummyScript(runner)
    runner.execute()
    runner.logger.close()

    log_file = find_latest_log('cd_etl_Runner')
    with open(log_file, 'r') as f:
        assert len(f.readlines()) > 6


def test_retrieve_study_list_every_5_secs():

    runner = Runner(params={'interval': 5, 'time_period': 10})
    runner.script = RetrieveStudyListScript(runner)
    runner.execute()
    runner.logger.close()

    log_file = find_latest_log('cd_etl_Runner')

    count = 0
    with open(log_file, 'r') as f:
        for line in f.readlines():
            if 'study_id' in line.strip():
                count += 1
    assert count > 0


def test_retrieve_dashboard_data():

    runner = Runner(params={'interval': 0, 'time_period': 0})
    runner.script = RetrieveDashboardDataScript(runner)
    runner.execute()
    runner.logger.close()

    print('Ok')

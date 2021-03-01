import os

from types import SimpleNamespace

from castordashboard.etl import ScriptRunner
from castordashboard.etl import DummyScript
from castordashboard.etl import RetrieveStudyListScript
from castordashboard.etl import RetrieveDashboardDataScript


def find_latest_log(prefix):
    log_file = None
    max_x = 0
    for f in os.listdir('.'):
        if f.startswith(prefix):
            x = int(f.split('_')[2][:-4])
            if x > max_x:
                max_x = x
                log_file = f
    print('Latest log file: {}'.format(log_file))
    return log_file


def test_periodic_execution():

    runner = ScriptRunner(interval=0, time_period=0)
    runner.script = DummyScript(runner, {})
    runner.execute()
    runner.logger.close()

    log_file = find_latest_log('cd_etl_Runner')
    with open(log_file, 'r') as f:
        assert len(f.readlines()) == 6

    runner = ScriptRunner(interval=1, time_period=5)
    runner.script = DummyScript(runner, {})
    runner.execute()
    runner.logger.close()

    log_file = find_latest_log('log_etl')
    with open(log_file, 'r') as f:
        assert len(f.readlines()) == 18


def test_retrieve_study_list_every_5_secs():

    runner = ScriptRunner(interval=5, time_period=10)
    runner.script = RetrieveStudyListScript(runner, {})
    runner.execute()
    runner.logger.close()

    log_file = find_latest_log('log_etl')

    count = 0
    with open(log_file, 'r') as f:
        for line in f.readlines():
            if 'study_id' in line.strip():
                count += 1
    assert count > 0


def test_retrieve_dashboard_data_liver():

    params = {
        'study_name': 'ESPRESSO_v2.0_DHBA',
        'year_begin': 2014,
        'year_end': 2018,
        'field_name': 'dhba_datok',
        'output_dir': '/tmp/castordashboard',
        'output_json': 'histogram_dhba.json',
        'use_cache': False,
        'verbose': True,
    }

    runner = ScriptRunner()
    runner.script = RetrieveDashboardDataScript(runner, params)
    runner.execute()
    runner.logger.close()

    params = SimpleNamespace(**params)
    assert os.path.isfile(os.path.join(params.output_dir, params.output_json))


def test_retrieve_dashboard_data_pancreas():

    params = {
        'study_name': 'ESPRESSO_v2.0_DPCA',
        'year_begin': 2014,
        'year_end': 2018,
        'field_name': 'dpca_datok',
        'output_dir': '/tmp/castordashboard',
        'output_json': 'histogram_dpca.json',
        'use_cache': False,
        'verbose': True,
    }

    runner = ScriptRunner()
    runner.script = RetrieveDashboardDataScript(runner, params)
    runner.execute()
    runner.logger.close()

    params = SimpleNamespace(**params)
    assert os.path.isfile(os.path.join(params.output_dir, params.output_json))


def test_main():

    import sys
    import json
    from castordashboard.etl import script_runner

    with open('params.json', 'w') as f:
        json.dump({
            'script': 'castordashboard.etl.scripts.DummyScript',
            'study_name': 'ESPRESSO_v2.0_DPCA',
            'output_dir': '/tmp/castordashboard',
            'output_json': 'histogram_dpca.json',
            'use_cache': False,
            'verbose': False,
        }, f)

    sys.argv = ['script_runner.py', 'params.json']

    script_runner.main()

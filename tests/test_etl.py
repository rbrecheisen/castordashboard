import os
import time

from castordashboard.etl import Runner, DummyScript


def test_params():
    runner = Runner(params={'name': 'value'})
    print(runner.params.name)


def test_periodic_execution():

    runner = Runner(params={'interval': 1, 'time_period': 5})
    runner.script = DummyScript()
    runner.execute()
    runner.logger.close()

    log_file = None
    max_x = 0
    for f in os.listdir('.'):
        if f.startswith('cd_etl_Runner'):
            x = int(f.split('_')[3][:-4])
            if x > max_x:
                max_x = x
                log_file = f
    print(log_file)

    with open(log_file, 'r') as f:
        assert len(f.readlines()) == 15

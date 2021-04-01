from etl.script_runner import ScriptRunner
from barbell2light import Logger


def test_script_runner():
    params = {
        'scripts': [
            'RetrieveProcedureCountsAndComplicationsPerQuarterScript',
            'RetrieveProcedureComplicationsPerQuarterScript',
        ],
        'output_dir': '/tmp/castordashboard',
        'log_dir': '/tmp/castordashboard/logs',
        'use_cache': False,
        'verbose': False,
    }
    script_runner = ScriptRunner(params)
    script_runner.execute()

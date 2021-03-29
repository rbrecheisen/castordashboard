from etl.scripts.procedurecomplications import RetrieveProcedureComplicationsScript
from barbell2light import Logger


def test_script():
    script = RetrieveProcedureComplicationsScript(
        'RetrieveProcedureComplicationsScript', Logger(to_dir='/tmp/castordashboard/logs'), {
            'scripts': [
                'RetrieveProcedureComplicationsScript'
            ],
            'output_dir': '/tmp/castordashboard',
            'log_dir': '/tmp/castordashboard/logs',
            'use_cache': False,
            'verbose': False,
        })
    script.execute()

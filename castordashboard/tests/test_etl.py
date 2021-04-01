from etl.scripts.retrieveprocedurecomplicationsscript import RetrieveProcedureComplicationsPerQuarterScript
from barbell2light import Logger


def test_script():
    params = {
        'scripts': [
            'RetrieveProcedureComplicationsPerQuarterScript'
        ],
        'output_dir': '/tmp/castordashboard',
        'log_dir': '/tmp/castordashboard/logs',
        'use_cache': False,
        'verbose': False,
    }
    script = RetrieveProcedureComplicationsPerQuarterScript(
        'RetrieveProcedureComplicationsPerQuarterScript', Logger(to_dir='/tmp/castordashboard/logs'), params)
    script.execute()

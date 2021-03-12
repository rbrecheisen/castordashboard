import os
import json
import argparse
import importlib
import datetime

from barbell2.utils import Logger, current_time_secs, elapsed_secs


class ScriptRunner:

    def __init__(self, params):
        self.params = params
        self.scripts = []
        self.logger = Logger(prefix='log_etl')

    def get_output_dir(self):
        os.makedirs(self.params['output_dir'], exist_ok=True)
        now = datetime.datetime.now()
        timestamp = '{}'.format(now.strftime('%Y%m%d%H%M%S'))
        os.makedirs(os.path.join(self.params['output_dir'], timestamp), exist_ok=True)
        output_dir = os.path.join(self.params['output_dir'], timestamp)
        return output_dir

    def execute(self):
        if len(self.scripts) == 0:
            self.logger.print('Nothing to execute')
            return
        output_dir = self.get_output_dir()
        start_overall = current_time_secs()
        for script in self.scripts:
            self.logger.print('Starting script {}'.format(script.name))
            start = current_time_secs()
            script.execute(output_dir)
            self.logger.print(
                'Script finished after {} seconds'.format(elapsed_secs(start)))
        self.logger.print(
            'Elapsed overall: {} seconds'.format(elapsed_secs(start_overall)))
        os.system('touch {}'.format(os.path.join(output_dir, 'finished.txt')))


HELP = """
Path to parameter file (default: params.json)

Example parameter file:

{
    "scripts": {
        "DummyScript": {},
        "RetrieveStudyListScript": {},
        "RetrieveProcedureCountsAndComplicationsPerQuarterScript": {
            "study_name": "ESPRESSO_v2.0_DPCA",
            "surgery_date_field_name": "dpca_datok",
            "complications_field_name": "dpca_compl"
        }
    },
    "output_dir": "./castordashboard_data",
    "use_cache": false,
    "verbose": true,
    "websocket_origin": "137.120.191.233:5006",
    "port_nr": 5006
}

The "scripts" item contains a dictionary of script (class) names as keys and various script-specific
settings as values.  For example, the RetrieveProcedureCountsAndComplicationsPerQuarterScript script
requires a study name to access the right study in Castor EDC.

The other parameter settings specify where to store the script output JSON data. 
"""


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--params', help=HELP, default='params.json')
    args = parser.parse_args()
    with open(args.params, 'r') as f:
        params = json.load(f)

    runner = ScriptRunner(params)
    for script_name in params['scripts'].keys():
        script = getattr(importlib.import_module('castordashboard.etl.scripts'), script_name)
        runner.scripts.append(script(script_name, runner, params))
    runner.execute()


if __name__ == '__main__':
    main()

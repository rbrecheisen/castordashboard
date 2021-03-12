from barbell2.castorclient import CastorClient
from . import BaseScript


class RetrieveStudyListScript(BaseScript):

    def __init__(self, name, runner, params):
        super(RetrieveStudyListScript, self).__init__(name, runner, params)

    def execute(self, output_dir):
        client = CastorClient()
        study_list = client.get_studies()
        data = []
        for study in study_list:
            data.append(str(study))
        self.save_to_json(data, output_dir)

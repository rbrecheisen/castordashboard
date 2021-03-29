from barbell2light.castorclient import CastorClient
from . import BaseScript


class RetrieveStudyListScript(BaseScript):

    def __init__(self, name, logger, params):
        super(RetrieveStudyListScript, self).__init__(name, logger, params)

    def execute(self):
        client = CastorClient()
        study_list = client.get_studies()
        data = []
        for study in study_list:
            data.append(str(study))
        self.save_to_json(data, self.params['output_dir'])

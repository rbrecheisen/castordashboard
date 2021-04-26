import os
import json

from barbell2light.castorclient import CastorClient
from .basescript import BaseScript


class RetrieveProcedureComplicationsPerQuarterScript(BaseScript):

    def __init__(self, logger, output_dir):
        name = self.__class__.__name__
        super(RetrieveProcedureComplicationsPerQuarterScript, self).__init__(name, logger)
        self.client = CastorClient(log_dir='.')
        self.study_id = self.client.get_study_id(os.environ['CASTOR_DASHBOARD_STUDY_NAME'])
        self.output_dir = output_dir

    @staticmethod
    def get_numerical_representation(date_str):
        items = date_str.split('-')
        return int('{}{}{}'.format(items[2], items[1], items[0]))

    def get_earliest_and_latest_date(self, date_list):
        min_date = 999999999
        min_date_str = ''
        max_date = 0
        max_date_str = ''
        for d in date_list:
            x = self.get_numerical_representation(d)
            if x < min_date:
                min_date = x
                min_date_str = d
            if x > max_date:
                max_date = x
                max_date_str = d
        return min_date_str, max_date_str

    @staticmethod
    def get_year(date_str):
        return int(date_str.split('-')[2])

    # @staticmethod
    # def get_month(date_str):
    #     return int(date_str.split('-')[1])

    def get_histogram(self, year_begin, year_end, surgery_dates, complications):
        histogram = {}
        for year in range(year_begin, year_end + 1):
            histogram[year] = {'comp_y': 0, 'comp_n': 0}
        for i in range(len(surgery_dates)):
            d = surgery_dates[i]
            c = complications[i]
            y = self.get_year(d)
            if y in histogram.keys():
                if c == 1:
                    histogram[y]['comp_y'] += 1
                else:
                    histogram[y]['comp_n'] += 1
        return histogram

    @staticmethod
    def flatten_histogram(histogram):
        histogram_new = {'years': [], 'comp_y': [], 'comp_n': []}
        for y in histogram.keys():
            histogram_new['years'].append(y)
            histogram_new['comp_y'].append(histogram[y]['comp_y'])
            histogram_new['comp_n'].append(histogram[y]['comp_n'])
        return histogram_new

    # def get_histogram(self, year_begin, year_end, surgery_dates, complications):
    #     histogram = {}
    #     for year in range(year_begin, year_end + 1):
    #         histogram[year] = {
    #             '1_2_3': {'comp_y': 0, 'comp_n': 0},
    #             '4_5_6': {'comp_y': 0, 'comp_n': 0},
    #             '7_8_9': {'comp_y': 0, 'comp_n': 0},
    #             '10_11_12': {'comp_y': 0, 'comp_n': 0},
    #         }
    #     for i in range(len(surgery_dates)):
    #         d = surgery_dates[i]
    #         c = complications[i]
    #         y = self.get_year(d)
    #         m = str(self.get_month(d))
    #         if y in histogram.keys():
    #             for q in histogram[y].keys():
    #                 q_items = q.split('_')
    #                 if m in q_items:
    #                     if c == 1:
    #                         histogram[y][q]['comp_y'] += 1
    #                     else:
    #                         histogram[y][q]['comp_n'] += 1
    #     return histogram
    #
    # @staticmethod
    # def get_quarter(k):
    #     if k == '1_2_3':
    #         return 'q1'
    #     if k == '4_5_6':
    #         return 'q2'
    #     if k == '7_8_9':
    #         return 'q3'
    #     return 'q4'
    #
    # def flatten_histogram(self, histogram):
    #     histogram_new = {'quarters': [], 'comp_y': [], 'comp_n': []}
    #     for y in histogram.keys():
    #         for k in histogram[y].keys():
    #             q = self.get_quarter(k)
    #             q = '{}_{}'.format(y, q)
    #             histogram_new['quarters'].append(q)
    #             histogram_new['comp_y'].append(histogram[y][k]['comp_y'])
    #             histogram_new['comp_n'].append(histogram[y][k]['comp_n'])
    #     return histogram_new

    def get_data(self, fields, option_groups, records, use_cache=False):

        # Use only for debugging!
        if use_cache and os.path.isfile('cached_data.json'):
            with open('cached_data.json', 'r') as f:
                return json.load(f)

        data = {'dpca': {}}

        # Get field IDs for the DPCA variables of interest
        proc_type_id = self.client.get_field_id('dpca_typok', fields)
        surgery_date_id = self.client.get_field_id('dpca_datok', fields)
        complications_id = self.client.get_field_id('dpca_compl', fields)

        # Iterate through each record of the data (this was loaded in a previous step, either
        # from cache or Castor directly)
        for record in records:

            # Get the procedure type data for this record. It's an option group in this case so
            # we'll get an index value. We need to look up the procedure type name.
            proc_type_data = self.client.get_field_data(self.study_id, record['id'], proc_type_id)

            # Only if there's a 'value' key, does the procedure type have a value.
            if 'value' in proc_type_data.keys():

                # Get procedure type name
                proc_type_name = self.client.get_option_name(proc_type_data['value'], 'dpca_typok', option_groups)

                # If procedure type name was not encountered before, create an empty dictionary item for it
                # with empty lists for surgery dates and complications
                if proc_type_name not in data['dpca'].keys():
                    data['dpca'][proc_type_name] = {
                        'surgery_dates': [],
                        'complications': [],
                    }

                # Get surgery date
                surgery_date_data = self.client.get_field_data(self.study_id, record['id'], surgery_date_id)

                if 'value' in surgery_date_data.keys():

                    # If surgery date has value, get complications (yes/no)
                    complications_data = self.client.get_field_data(self.study_id, record['id'], complications_id)

                    if 'value' in complications_data.keys():

                        # If complications has value as well, append the values for surgery date and complications
                        # to the lists for this procedure type.
                        d = surgery_date_data['value']
                        c = int(complications_data['value'])
                        data['dpca'][proc_type_name]['surgery_dates'].append(d)
                        data['dpca'][proc_type_name]['complications'].append(c)

                        self.logger.print('{}: surgery_date = {}, complications = {}'.format(record['id'], d, c))

        # Only for debugging
        if use_cache:
            with open('cached_data.json', 'w') as f:
                json.dump(data, f, indent=4)

        return data

    @staticmethod
    def group_procedures(data):

        PROC = [
            "Pylorus-preserving pancreaticoduodenectomy (PPPD)",  # 0
            "Pylorus ring resection pancreaticoduodenectomy (PRPD)",  # 1
            "Enucleation pancreas tumor",  # 2
            "Classical Whipple",  # 3
            "Pancreatic corpus/tail resection",  # 4
            "Total pancreatectomy",  # 5
        ]

        # Define new set of (grouped) procedures
        new_data = {
            'dpca': {
                'Whipple': {},
                'Pancreas tail resection': {},
                'Total pancreatectomy': {},
                'All procedures': {},
            },
        }

        # Iterate through original procedures and put them in the right place
        for proc_type in data['dpca'].keys():

            # Determine key for new dictionary
            key = None
            if proc_type == PROC[0] or proc_type == PROC[1] or proc_type == PROC[2] or proc_type == PROC[3]:
                key = 'Whipple'
            if proc_type == PROC[4]:
                key = 'Pancreas tail resection'
            if proc_type == PROC[5]:
                key = 'Total pancreatectomy'

            # If key is still None, skip iteration
            if key is None:
                continue

            # Copy year and complication info to new dictionary
            for i in range(len(data['dpca'][proc_type]['years'])):

                year = data['dpca'][proc_type]['years'][i]
                comp_y = data['dpca'][proc_type]['comp_y'][i]
                comp_n = data['dpca'][proc_type]['comp_n'][i]

                if year not in new_data['dpca'][key].keys():
                    new_data['dpca'][key][year] = {'comp_y': 0, 'comp_n': 0}
                if year not in new_data['dpca']['All procedures'].keys():
                    new_data['dpca']['All procedures'][year] = {'comp_y': 0, 'comp_n': 0}

                new_data['dpca'][key][year]['comp_y'] += comp_y
                new_data['dpca'][key][year]['comp_n'] += comp_n
                new_data['dpca']['All procedures'][year]['comp_y'] += comp_y
                new_data['dpca']['All procedures'][year]['comp_n'] += comp_n

        return new_data

    def execute(self):

        # Get Castor field definitions. Use cache if configured
        fields = self.client.get_fields(self.study_id, use_cache=True, verbose=True)

        # Get Castor records and option groups (from cache is configured)
        records = self.client.get_records(self.study_id, use_cache=True, verbose=True)
        option_groups = self.client.get_option_groups(self.study_id, verbose=True)

        # Get Castor data. We always get it directly from Castor, so no caching. This is the raw data
        # so we should save it to JSON. The dashboard app can then decide for itself what to display.
        data = self.get_data(fields, option_groups, records, use_cache=True)

        # Run through the collected data and refactor the dictionary to list procedure counts per
        # quarter for each procedure type separately.
        new_data = {'dpca': {}}
        for proc_type in data['dpca'].keys():
            proc_data = data['dpca'][proc_type]
            date_begin, date_end = self.get_earliest_and_latest_date(proc_data['surgery_dates'])
            year_begin, year_end = self.get_year(date_begin), self.get_year(date_end)
            histogram = self.get_histogram(year_begin, year_end, proc_data['surgery_dates'], proc_data['complications'])
            histogram = self.flatten_histogram(histogram)
            new_data['dpca'][proc_type] = histogram

        # Group procedures differently, e.g. serveral procedures should be classified as "Whipple" procedures
        new_data = self.group_procedures(new_data)

        for proc_type in new_data['dpca'].keys():
            histogram = self.flatten_histogram(new_data['dpca'][proc_type])
            new_data['dpca'][proc_type] = histogram

        # Save data to JSON
        self.save_to_json(new_data, self.output_dir)

# dpca_typok
# ==========
# Pylorus-preserving pancreaticoduodenectomy (PPPD)
# Classical Whipple
# Pylorus ring resection pancreaticoduodenectomy (PRPD)
# Pancreatic corpus/tail resection
# Central pancreas resection
# Total pancreatectomy
# Enucleation pancreas tumor
# Other
# Unknown

# dhba_typok
# ==========
# Resection
# Resection + RFA
# Open-closed

# dhba_procok
# ===========
# Resection
# Ablation
# Resection and ablation
# Open/closed

# dhba_procok1
# ============
# Resection bile duct
# Resection bile duct + liver resection
# Resection bile duct + liver resection + pancreas resection
# Irresectable during probe laparoscopy
# Resection galbladder + liver resection

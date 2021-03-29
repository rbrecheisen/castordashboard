import os
import json
from barbell2light.castorclient import CastorClient
from . import BaseScript


class RetrieveProcedureComplicationsScript(BaseScript):

    def __init__(self, name, logger, params):
        super(RetrieveProcedureComplicationsScript, self).__init__(name, logger, params)
        self.client = CastorClient(log_dir=self.params['log_dir'])
        self.study_id = self.client.get_study_id('ESPRESSO_v2.0_DPCA')
        self.surgery_date_dpca = 'dpca_datok'
        self.surgery_date_dhba = 'dhba_datok1'  # dhba_datok = date resection primary tumor
        self.complications_dpba = 'dpca_compl'
        self.complications_dhba = 'dhba_compl'
        self.procedure_type_dpca = 'dpca_typok'
        self.procedure_type_dhba = 'dhba_procok'
        self.procedure_type_dhba_2014 = 'dhba_typok'

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

    @staticmethod
    def get_month(date_str):
        return int(date_str.split('-')[1])

    def get_histogram(self, year_begin, year_end, surgery_dates, complications):
        histogram = {}
        for year in range(year_begin, year_end + 1):
            histogram[year] = {
                '1_2_3': {'comp_y': 0, 'comp_n': 0},
                '4_5_6': {'comp_y': 0, 'comp_n': 0},
                '7_8_9': {'comp_y': 0, 'comp_n': 0},
                '10_11_12': {'comp_y': 0, 'comp_n': 0},
            }
        for i in range(len(surgery_dates)):
            d = surgery_dates[i]
            c = complications[i]
            y = self.get_year(d)
            m = str(self.get_month(d))
            if y in histogram.keys():
                for q in histogram[y].keys():
                    q_items = q.split('_')
                    if m in q_items:
                        if c == 1:
                            histogram[y][q]['comp_y'] += 1
                        else:
                            histogram[y][q]['comp_n'] += 1
        return histogram

    @staticmethod
    def get_quarter(k):
        if k == '1_2_3':
            return 'q1'
        if k == '4_5_6':
            return 'q2'
        if k == '7_8_9':
            return 'q3'
        return 'q4'

    def flatten_histogram(self, histogram):
        histogram_new = {'quarters': [], 'comp_y': [], 'comp_n': []}
        for y in histogram.keys():
            for k in histogram[y].keys():
                q = self.get_quarter(k)
                q = '{}_{}'.format(y, q)
                histogram_new['quarters'].append(q)
                histogram_new['comp_y'].append(histogram[y][k]['comp_y'])
                histogram_new['comp_n'].append(histogram[y][k]['comp_n'])
        return histogram_new

    def get_data(self, fields, option_groups, records, use_cache=True):
        if use_cache and os.path.isfile('/tmp/castordashboard/cache.json'):
            with open('/tmp/castordashboard/cache.json', 'r') as f:
                return json.load(f)
        data = {'dpca': {}, 'dhba': {}}
        field_id = self.client.get_field_id('dpca_typok', fields)
        surgery_date_id = self.client.get_field_id('dpca_datok', fields)
        complications_id = self.client.get_field_id('dpca_compl', fields)
        for record in records:
            field_data = self.client.get_field_data(self.study_id, record['id'], field_id)
            if 'value' in field_data.keys():
                option_name = self.client.get_option_name(field_data['value'], 'dpca_typok', option_groups)
                if option_name not in data['dpca'].keys():
                    data['dpca'][option_name] = {
                        'surgery_dates': [],
                        'complications': [],
                    }
                surgery_date_data = self.client.get_field_data(self.study_id, record['id'], surgery_date_id)
                if 'value' in surgery_date_data.keys():
                    complications_data = self.client.get_field_data(self.study_id, record['id'], complications_id)
                    if 'value' in complications_data.keys():
                        d = surgery_date_data['value']
                        c = int(complications_data['value'])
                        data['dpca'][option_name]['surgery_dates'].append(d)
                        data['dpca'][option_name]['complications'].append(c)
                        self.logger.print('{}: surgery_date = {}, complications = {}'.format(record['id'], d, c))
        with open('/tmp/castordashboard/cache.json', 'w') as f:
            json.dump(data, f, indent=4)
        return data

    def execute(self):
        use_cache = True
        verbose = True if 'verbose' in self.params.keys() and self.params['verbose'] else False
        fields = self.client.get_fields(self.study_id, use_cache=use_cache, verbose=verbose)
        records = self.client.get_records(self.study_id, use_cache=use_cache, verbose=verbose)
        option_groups = self.client.get_option_groups(self.study_id, verbose=verbose)
        data = self.get_data(fields, option_groups, records, use_cache=use_cache)
        for proc_type in data['dpca'].keys():
            proc_data = data['dpca'][proc_type]
            date_begin, date_end = self.get_earliest_and_latest_date(proc_data['surgery_dates'])
            year_begin, year_end = self.get_year(date_begin), self.get_year(date_end)
            histogram = self.get_histogram(year_begin, year_end, proc_data['surgery_dates'], proc_data['complications'])
            histogram = self.flatten_histogram(histogram)
            # TODO: I was here!
        self.save_to_json(data, self.params['output_dir'])

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

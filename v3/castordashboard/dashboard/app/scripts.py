import os
import json

from django.conf import settings
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource


class BaseScript:

    def __init__(self, name):
        self.name = name
        self.timestamp = None
        self.params = self.load_params()

    @staticmethod
    def load_params():
        with open(settings.PARAMS_FILE_PATH, 'r') as f:
            return json.load(f)

    @staticmethod
    def find_most_recent_data_dir():
        ld = None
        max_x = 0
        for d in os.listdir(os.environ['OUTPUT_DIR']):
            try:
                x = int(d)
                d = os.path.join(os.environ['OUTPUT_DIR'], d)
                if os.path.isfile(os.path.join(d, 'finished.txt')) and x > max_x:
                    ld = d
                    max_x = x
            except ValueError:
                pass
        print('Latest (finished) directory: {}'.format(ld))
        return ld

    def load_data(self):
        data_dir = self.find_most_recent_data_dir()
        if data_dir is not None:
            with open(os.path.join(data_dir, '{}.json'.format(self.name)), 'r') as f:
                self.timestamp = data_dir.split(os.path.sep)[-1]
                return json.load(f)
        return None

    def get_plots(self):
        raise NotImplementedError()


class RetrieveProcedureComplicationsDPCA(BaseScript):

    def __init__(self):
        super(RetrieveProcedureComplicationsDPCA, self).__init__(name='RetrieveProcedureComplicationsDPCA')
        self.title = 'Pancreatic Procedure Complications per Year'

    def get_plots(self):

        data = self.load_data()
        plots = []

        self.title += ' ({})'.format(self.timestamp)

        for proc_type in data['dpca'].keys():

            x = data['dpca'][proc_type]

            years = [str(xx) for xx in x['years']]  # IMPORTANT: convert this to strings because it's a categorical
            comp_n = x['comp_n']
            comp_y = x['comp_y']

            colors = ['#718dbf', '#e84d60']

            source = ColumnDataSource(data={
                'years': years,
                'comp_n': comp_n,
                'comp_y': comp_y,
            })

            p = figure(
                x_range=years,
                plot_width=500, plot_height=500,
                title=proc_type,
            )

            p.vbar_stack(
                stackers=['comp_y', 'comp_n'],
                x='years',
                width=0.9,
                color=colors,
                source=source,
                legend_label=['Complications YES', 'Complications NO'])

            p.title.text_font_size = '16pt'
            p.xaxis.major_label_orientation = 'vertical'
            p.y_range.start = 0
            p.x_range.range_padding = 0.1
            p.xgrid.grid_line_color = None
            p.axis.minor_tick_line_color = None
            p.outline_line_color = None
            p.legend.location = "top_left"
            p.legend.orientation = "horizontal"

            plots.append(p)

        return plots


def get_script(name):
    scripts = {
        'RetrieveProcedureComplicationsDPCA': RetrieveProcedureComplicationsDPCA(),
    }
    return scripts[name]

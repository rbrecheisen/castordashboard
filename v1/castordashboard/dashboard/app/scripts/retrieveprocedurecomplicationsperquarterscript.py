from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from .basescript import BaseScript


class RetrieveProcedureComplicationsPerQuarterScript(BaseScript):

    def __init__(self):
        super(RetrieveProcedureComplicationsPerQuarterScript, self).__init__(
            name='RetrieveProcedureComplicationsPerQuarterScript')
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

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from .basescript import BaseScript


class RetrieveProcedureCountsAndComplicationsPerQuarterScript(BaseScript):

    def __init__(self):
        super(RetrieveProcedureCountsAndComplicationsPerQuarterScript, self).__init__(
            name='RetrieveProcedureCountsAndComplicationsPerQuarterScript')
        self.title = 'Procedure Counts and Overall Complications'

    def get_plots(self):

        data = self.load_data()

        self.title += ' ({})'.format(self.timestamp)

        quarters = data['quarters']
        comp_n = data['comp_n']
        comp_y = data['comp_y']

        colors = ['#718dbf', '#e84d60']

        source = ColumnDataSource(data={
            'quarters': quarters,
            'comp_n': comp_n,
            'comp_y': comp_y,
        })

        p = figure(
            x_range=quarters,
            plot_width=1000, plot_height=500,
            title='Pancreatic procedure counts and complications per quarter ({})'.format(self.timestamp),
        )

        p.vbar_stack(
            stackers=['comp_y', 'comp_n'],
            x='quarters',
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

        return [p]

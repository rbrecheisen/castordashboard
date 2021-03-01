import os
import json
import numpy as np

from bokeh.layouts import column
from bokeh.models import ColumnDataSource
from bokeh.plotting import curdoc, figure


NR_YEARS = 5

NR_QUARTERS = 4 * NR_YEARS


def load_json(file_path):
    if os.path.isfile(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return None


pancreas_histogram = load_json('/tmp/castordashboard/20210301105505/histogram_dpca.json')
pancreas_quarters = list(pancreas_histogram.keys())[-NR_QUARTERS:]
pancreas_counts = list(pancreas_histogram.values())[-NR_QUARTERS:]
pancreas_source = ColumnDataSource(data={'quarters': pancreas_quarters, 'counts': pancreas_counts})
pancreas_p = figure(
    x_range=pancreas_quarters,
    y_range=(0, np.max(pancreas_counts) + 1),
    plot_height=300,
    title='Quarter counts pancreas',
)
pancreas_p.vbar(x='quarters', top='counts', width=0.9, source=pancreas_source)
pancreas_p.xaxis.major_label_orientation = 'vertical'


def main():
    curdoc().add_root(column(pancreas_p))


main()

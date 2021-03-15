import os
import json

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.embed import components
from bokeh.palettes import Spectral6
from bokeh.transform import factor_cmap


def load_json(file_path):
    if os.path.isfile(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return None


def find_latest_finished_dir(root_dir):
    ld = None
    max_x = 0
    for d in os.listdir(root_dir):
        try:
            x = int(d)
            d = os.path.join(root_dir, d)
            if os.path.isfile(os.path.join(d, 'finished.txt')) and x > max_x:
                ld = d
                max_x = x
        except ValueError:
            pass
    print('Latest (finished) directory: {}'.format(ld))
    return ld


def register(request):
    context = {}
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    context['form'] = form
    return render(request, 'registration/register.html', context)


@login_required
def dashboard(request):

    params = load_json('/data/params.json')
    latest_dir = find_latest_finished_dir(params['output_dir'])
    histogram = load_json(os.path.join(latest_dir, 'RetrieveProcedureCountsAndComplicationsPerQuarterScript.json'))
    timestamp = latest_dir.split(os.path.sep)[-1]

    quarters = histogram['quarters']
    comp_n = histogram['comp_n']
    comp_y = histogram['comp_y']

    colors = ['#718dbf', '#e84d60']

    source = ColumnDataSource(data={
        'quarters': quarters,
        'comp_n': comp_n,
        'comp_y': comp_y,
    })

    p = figure(
        x_range=quarters,
        plot_width=1000, plot_height=500,
        title='Pancreatic procedure counts and complications per quarter ({})'.format(timestamp),
    )

    p.vbar_stack(
        stackers=['comp_y', 'comp_n'],
        x='quarters',
        width=0.9,
        color=colors,
        source=source,
        legend_label=['Complications YES', 'Complications NO'])

    p.xaxis.major_label_orientation = 'vertical'
    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    p.axis.minor_tick_line_color = None
    p.outline_line_color = None
    p.legend.location = "top_left"
    p.legend.orientation = "horizontal"

    script, div = components(p)

    return render(request, 'dashboard.html', {'script': script, 'div': div})


@login_required
def dashboard_old(request):
    fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
    years = ['2015', '2016', '2017']
    data = {
        'fruits': fruits,
        '2015': [2, 1, 4, 3, 2, 4],
        '2016': [5, 3, 3, 2, 4, 6],
        '2017': [3, 2, 4, 4, 5, 3],
    }
    x_values = [(fruit, year) for fruit in fruits for year in years]
    counts = sum(zip(data['2015'], data['2016'], data['2017']), ())
    source = ColumnDataSource(data=dict(x=x_values, counts=counts))
    plot = figure(
        x_range=FactorRange(*x_values),
        plot_height=250,
        title='Fruit counts per year',
        toolbar_location=None,
        tools='',
    )
    plot.vbar(
        x='x',
        top='counts',
        width=0.9,
        source=source,
        line_color='white',
        fill_color=factor_cmap(
            'x',
            palette=Spectral6,
            factors=years,
            start=1,
            end=2
        )
    )
    plot.y_range.start = 0
    plot.x_range.range_padding = 0.1
    plot.xaxis.major_label_orientation = 1
    plot.xgrid.grid_line_color = None
    script, div = components(plot)
    return render(request, 'dashboard.html', {'script': script, 'div': div})

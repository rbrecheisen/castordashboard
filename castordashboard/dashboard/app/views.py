from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.embed import components
from bokeh.palettes import Spectral6
from bokeh.transform import factor_cmap


def register(request):
    context = {}
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('images')
    context['form'] = form
    return render(request, 'registration/register.html', context)


@login_required
def dashboard(request):
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

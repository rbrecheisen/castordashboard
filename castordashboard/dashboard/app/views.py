from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from bokeh.embed import components
from .scripts.retrieveprocedurecountsandcomplicationsperquarterscript \
    import RetrieveProcedureCountsAndComplicationsPerQuarterScript


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

    script = RetrieveProcedureCountsAndComplicationsPerQuarterScript()

    html_scripts = []
    html_divs = []

    for p in script.get_plots():
        s, d = components(p)
        html_scripts.append(s)
        html_divs.append(d)

    return render(request, 'dashboard.html', {'scripts': html_scripts, 'divs': html_divs})

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from bokeh.embed import components
from .scripts import BaseScript, get_script


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


def load_scripts():
    params = BaseScript.load_params()
    return params['scripts']


@login_required
def dashboard(request):
    script_name = request.GET.get('script_name', None)
    if script_name is None:
        script_names = load_scripts()
        return render(request, 'dashboard.html', {'script_names': script_names})
    else:
        script = get_script(script_name)
        html_scripts = []
        html_divs = []
        for p in script.get_plots():
            s, d = components(p)
            html_scripts.append(s)
            html_divs.append(d)
        return render(request, 'dashboard.html', {
            'scripts': html_scripts,
            'divs': html_divs,
            'title': script.title,
        })

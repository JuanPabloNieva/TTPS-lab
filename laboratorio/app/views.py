from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.template.loader import get_template
from .forms import EstudioForm, LoginForm

# Create your views here.
def home(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            return render(request, 'estudio/index.html', {'form':form})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def estudios(request):
    if request.method == 'POST':
        form = EstudioForm(request.POST)
        if form.is_valid():
            return render(request, 'estudio/index.html')
    else:
        form = EstudioForm()
    return render(request, 'estudio/create.html', {'form': form})

def pacientes(request):
    return HttpResponse('Pacientes')

def empleados(request):
    return HttpResponse('Empleados')

def pendientes(request):
    return HttpResponse('Pendientes')

def login(request):
    form = LoginForm()
    return render(request, 'login.html', {'form': form})
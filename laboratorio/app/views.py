<<<<<<< HEAD
from django.shortcuts import render, HttpResponse
from .models import Paciente, ObraSocial
=======
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.template.loader import get_template
from .forms import EstudioForm, LoginForm
>>>>>>> 51cb4089b7ef2a8d483b33eded1a90c99a38ffea

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
    pacientes = Paciente.objects.all()
    return render(request, "pacientes/index.html", {"pacientes":pacientes})

def nuevoPaciente(request):
    obras = ObraSocial.objects.all()
    return render(request, 'pacientes/create.html', {"obras": obras})

def empleados(request):
    return HttpResponse('Empleados')

def pendientes(request):
    return HttpResponse('Pendientes')

def login(request):
    form = LoginForm()
    return render(request, 'login.html', {'form': form})
from django.shortcuts import render, HttpResponse
from .models import Paciente, ObraSocial

# Create your views here.
def home(request):
    return HttpResponse('Home')

def estudios(request):
    return HttpResponse('Estudios')

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
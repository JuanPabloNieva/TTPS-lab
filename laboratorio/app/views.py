from django.shortcuts import render, HttpResponse

# Create your views here.
def home(request):
    return HttpResponse('Home')

def estudios(request):
    return HttpResponse('Estudios')

def pacientes(request):
    return HttpResponse('Pacientes')

def empleados(request):
    return HttpResponse('Empleados')

def pendientes(request):
    return HttpResponse('Pendientes')
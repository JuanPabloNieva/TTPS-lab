from django.shortcuts import redirect, render, HttpResponseRedirect, HttpResponse
from django.urls.conf import path
from .models import Paciente, ObraSocial
from django.template.loader import get_template
from .forms import EstudioForm, LoginForm, PacienteForm
import random

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
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            #guardar en la BD
            nombre = request.POST['nombre']
            apellido = request.POST['apellido']
            dni = request.POST['dni']
            telefono = request.POST['telefono']
            obraSocial = ObraSocial.objects.filter(id=request.POST['obraSocial']).first()
            numeroAfiliado = random.randrange(99999)
            print(obraSocial)

            paciente = Paciente.objects.create(nombre=nombre, apellido=apellido, dni=dni, 
                telefono=telefono, obraSocial=obraSocial, numeroAfiliado=numeroAfiliado)

            return  redirect('/pacientes')
    else:
        form = PacienteForm()
    
    pacientes = Paciente.objects.all()
    return render(request, "pacientes/index.html", {"pacientes":pacientes})

def nuevoPaciente(request):
    obras = ObraSocial.objects.all()
    return render(request, 'pacientes/create.html', {"obras": obras})

def eliminarPaciente(request, id):
    paciente = Paciente.objects.get(id=id)
    paciente.delete()

    return redirect('/pacientes')

def editarPaciente(request, id):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            #guardar en la BD
            paciente = Paciente.objects.get(id=request.POST['id'])

            paciente.nombre = request.POST['nombre']
            paciente.apellido = request.POST['apellido']
            paciente.telefono = request.POST['telefono']
            paciente.dni = request.POST['dni']

            obraSocial = ObraSocial.objects.filter(id=request.POST['obraSocial']).first()
            paciente.obraSocial = obraSocial
            paciente.save()

            return redirect('/pacientes')
    else:
        form = PacienteForm()
    
    paciente = Paciente.objects.get(id=id)
    obras = ObraSocial.objects.all()
    return render(request, "pacientes/editar.html", {"obras":obras, "paciente":paciente})




def empleados(request):
    return HttpResponse('Empleados')

def pendientes(request):
    return HttpResponse('Pendientes')

def login(request):
    form = LoginForm()
    return render(request, 'login.html', {'form': form})
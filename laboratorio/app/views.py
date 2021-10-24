from django.shortcuts import redirect, render, HttpResponseRedirect, HttpResponse
from django.urls.conf import path
from .models import Paciente, ObraSocial, MedicoDerivante, TipoEstudio, Empleado, Estudio
from django.template.loader import get_template
from .forms import EstudioForm, LoginForm, PacienteForm
import random
from datetime import datetime

# Create your views here.


def home(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            return redirect('/estudios')
    else:
        form = LoginForm()
    return redirect('/login', {'form': form})


def estudios(request):
    estudios = Estudio.objects.all()
    return render(request, 'estudio/index.html', {'estudios': estudios})


def nuevoEstudio(request):
    if request.method == 'POST':
        form = EstudioForm(request.POST)
        if form.is_valid():
            medicoDerivante = MedicoDerivante.objects.filter(
                id=request.POST['medicoDerivante']).first()
            presupuesto = request.POST['presupuesto']
            # Deberia ser el empleado que esta en la session actualmente
            empleado = Empleado.objects.filter(id=1).first()
            fechaAlta = datetime.today()
            diagPresuntivo = request.POST['diagnosticoPresuntivo']
            estado = 'Esperando comprobante de pago'
            tipoEstudio = TipoEstudio.objects.filter(
                id=request.POST['tipoEstudio']).first()
            paciente = Paciente.objects.filter(
                id=request.POST['paciente']).first()
            if not paciente:
                pass
            else:
                estudio = Estudio.objects.create(medicoDerivante=medicoDerivante, presupuesto=presupuesto, estado=estado, tipoEstudio=tipoEstudio,
                                                 empleadoCarga=empleado, fechaAlta=fechaAlta, paciente=paciente, diagnosticoPresuntivo=diagPresuntivo)
            return redirect('/estudios')
    else:
        form = EstudioForm()
    medicosDerivantes = MedicoDerivante.objects.all()
    pacientes = Paciente.objects.all()
    tipoEstudios = TipoEstudio.objects.all()
    return render(request, 'estudio/create.html', {'form': form, 'md': medicosDerivantes, 'tipoEstudios': tipoEstudios})


def pacientes(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            # guardar en la BD
            nombre = request.POST['nombre']
            apellido = request.POST['apellido']
            dni = request.POST['dni']
            telefono = request.POST['telefono']
            obraSocial = ObraSocial.objects.filter(
                id=request.POST['obraSocial']).first()
            numeroAfiliado = random.randrange(99999)
            print(obraSocial)

            paciente = Paciente.objects.create(nombre=nombre, apellido=apellido, dni=dni,
                                               telefono=telefono, obraSocial=obraSocial, numeroAfiliado=numeroAfiliado)

            return redirect('/pacientes')
    else:
        form = PacienteForm()

    pacientes = Paciente.objects.all()
    return render(request, "pacientes/index.html", {"pacientes": pacientes})


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
            # guardar en la BD
            paciente = Paciente.objects.get(id=request.POST['id'])

            paciente.nombre = request.POST['nombre']
            paciente.apellido = request.POST['apellido']
            paciente.telefono = request.POST['telefono']
            paciente.dni = request.POST['dni']

            obraSocial = ObraSocial.objects.filter(
                id=request.POST['obraSocial']).first()
            paciente.obraSocial = obraSocial
            paciente.save()

            return redirect('/pacientes')
    else:
        form = PacienteForm()

    paciente = Paciente.objects.get(id=id)
    obras = ObraSocial.objects.all()
    return render(request, "pacientes/editar.html", {"obras": obras, "paciente": paciente})


def empleados(request):
    return HttpResponse('Empleados')


def pendientes(request):
    return HttpResponse('Pendientes')


def login(request):
    form = LoginForm()
    return render(request, 'login.html', {'form': form})

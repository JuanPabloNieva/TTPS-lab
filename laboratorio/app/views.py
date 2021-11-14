from django.conf.urls import url
from django.forms.forms import Form
from django.http.response import FileResponse
from django.shortcuts import redirect, render, HttpResponseRedirect, HttpResponse
from django.urls.conf import path
from django.template.loader import get_template
from django.contrib import messages
from .models import Comprobante, Consentimiento, ConsentimientoFirmado, Paciente, ObraSocial, MedicoDerivante, TipoEstudio, Empleado, Estudio, Historial, Estado, Turno

from .forms import EstudioForm, LoginForm, PacienteForm, HistorialForm, ComprobanteForm, ConsentimientoForm, TurnoFechaForm, TurnoForm
import random
import os
from laboratorio import settings
from datetime import date, datetime
from django.core.files.storage import Storage

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
            estado = Estado.objects.all().first()
            tipoEstudio = TipoEstudio.objects.filter(
                id=request.POST['tipoEstudio']).first()
            paciente = Paciente.objects.filter(
                id=request.POST['paciente']).first()
            try:
                estudio = Estudio.objects.create(medicoDerivante=medicoDerivante, presupuesto=presupuesto, estado=estado, tipoEstudio=tipoEstudio,
                                                 empleadoCarga=empleado, fechaAlta=fechaAlta, paciente=paciente, diagnosticoPresuntivo=diagPresuntivo)
            except:
                pass  # falta agregar excepción
            return redirect('/estudios')
    else:
        form = EstudioForm()
        medicosDerivantes = MedicoDerivante.objects.all()
        pacientes = Paciente.objects.all()
        tipoEstudios = TipoEstudio.objects.all()
        return render(request, 'estudio/create.html', {'form': form, 'md': medicosDerivantes, 'tipoEstudios': tipoEstudios})


def editarEstudio(request, id):
    if request.method == 'POST':
        estudio = Estudio.objects.get(id=id)
        medicoDerivante = MedicoDerivante.objects.get(
            id=request.POST['medicoDerivante'])
        estudio.medicoDerivante = medicoDerivante

        tipoEstudio = TipoEstudio.objects.get(id=request.POST['tipoEstudio'])
        estudio.tipoEstudio = tipoEstudio

        estudio.presupuesto = request.POST['presupuesto']
        estudio.diagnosticoPresuntivo = request.POST['diagnosticoPresuntivo']

        try:
            estudio.save()
        except:
            pass
        return redirect('/estudios')
    else:
        estudio = Estudio.objects.get(id=id)
        initial_dict = {
            'presupuesto': estudio.presupuesto,
            'diagnosticoPresuntivo': estudio.diagnosticoPresuntivo,
            'medicoDerivante': estudio.medicoDerivante,
            'tipoEstudio': estudio.tipoEstudio
        }
        form = EstudioForm(initial_dict)
        medicosDerivantes = MedicoDerivante.objects.all()
        pacientes = Paciente.objects.all()
        tipoEstudios = TipoEstudio.objects.all()
        return render(request, 'estudio/edit.html', {'form': form, 'md': medicosDerivantes, 'tipoEstudios': tipoEstudios, 'estudio': id})


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

# --------HISTORIAL----------


def historial(request):
    if request.method == 'POST':
        print(request.POST)
        form = HistorialForm(request.POST)
        print(form)
        if form.is_valid():
            # guardar en la BD
            paciente = Paciente.objects.filter(
                id=request.POST['paciente']).first()
            detalle = request.POST['texto']
            historial = Historial.objects.create(
                paciente=paciente, texto=detalle, fecha=datetime.now())
            id = paciente.id
            return redirect('/historial/paciente/'+str(id))
        else:
            error = "datos invalidos"
    else:
        form = HistorialForm()
    pacientes = Paciente.objects.all()
    return render(request, "historial/create.html", {"pacientes": pacientes, "error": error})


def nuevoHistorial(request, id):
    paciente = Paciente.objects.filter(id=id).first()
    return render(request, "historial/create.html", {"paciente": paciente})


def historialPaciente(request, id):
    paciente = Paciente.objects.filter(id=id).first()
    historial = Historial.objects.filter(paciente_id=paciente.id)
    return render(request, 'historial/index.html', {"paciente": paciente, "historial": historial})

# ------Pendientes---------


def pendientes(request):
    estudiosPendientes = []
    estudiosSinAbonar = Estudio.objects.filter(abonado=False)
    def is_valid(estudio): return estudio.estado.id > 7

    for estudio in estudiosSinAbonar:
        if is_valid(estudio):
            estudiosPendientes.append(estudio)
    return render(request, "estudio/pendientes.html", {"estudios": estudiosPendientes})


def pagarEstudios(request):
    print(request.POST)
    abonar = request.POST.getlist('estudios[]')

    for id in abonar:
        estudio = Estudio.objects.filter(id=id).first()
        estudio.abonado = True
        estudio.save()

    return redirect('/pendientes')

# ----------------------ESTADOS-----------------------------------------------


def CargarComprobante(request, id):
    estudio = Estudio.objects.filter(id=id).first()
    if request.method == 'POST':
        form = ComprobanteForm(request.POST, request.FILES)

        if form.is_valid():
            comprobante = Comprobante()
            comprobante.estudio = estudio
            comprobante.archivo = request.FILES['archivo']
            comprobante.save()

            estudio.estado = Estado.objects.filter(detalle="2").first()
            estudio.save()

            return redirect('/estudios')
    else:
        form = ComprobanteForm()

    return render(request, 'estudio/comprobante.html', {"form": form, "estudio": estudio})


def DescargarConsentimiento(request, id):
    estudio = Estudio.objects.filter(id=id).first()
    consentimiento = Consentimiento.objects.filter(
        tipoEstudio=estudio.tipoEstudio).first()
    file_path = os.path.join(settings.MEDIA_ROOT, consentimiento.archivo.name)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'attachment; filename=' + \
                os.path.basename(file_path)
            estudio.estado = Estado.objects.filter(detalle="3").first()
            estudio.save()
        return response


def CargarConsentimiento(request, id):
    estudio = Estudio.objects.filter(id=id).first()
    if request.method == 'POST':
        form = ConsentimientoForm(request.POST, request.FILES)

        if form.is_valid():
            consentimiento = ConsentimientoFirmado()
            consentimiento.estudio = estudio
            consentimiento.archivo = request.FILES['archivo']
            consentimiento.save()

            estudio.estado = Estado.objects.filter(detalle="4").first()
            estudio.save()

            return redirect('/estudios')
    else:
        form = ConsentimientoForm()

    return render(request, 'estudio/consentimiento.html', {"form": form, "estudio": estudio})

def SeleccionarTurno(request, id):
    estudio = Estudio.objects.filter(id=id).first()
    #HORARIOS IRIA EN SETTINGS PARA QUE SE REALICEN CAMBIOS EN UN UNICO LUGAR
    horarios = [('09:00:00', '09:00:00'), ('09:15:00', '09:15:00'), ('09:30:00', '09:30:00'), ('09:45:00', '09:45:00'), ('10:00:00', '10:00:00'), ('10:15:00', '10:15:00'), ('10:30:00', '10:30:00'),
                ('10:45:00', '10:45:00'), ('11:00:00', '11:00:00'), ('11:15:00', '11:15:00'), ('11:30:00', '11:30:00'), ('11:45:00', '11:45:00'), ('12:00:00', '12:00:00'), ('12:15:00', '12:15:00'), ('12:30:00', '12:30:00'), ('12:45:00', '12:45:00'), ('13:00:00', '13:00:00')]

    if request.method == 'POST':
        
        form = TurnoForm(horarios, request.POST)
        if form.is_valid():

            turno = Turno()
            turno.estudio = estudio
            turno.fecha = request.POST['fecha']
            print(request.POST['hora'])
            turno.hora = datetime.strptime(request.POST['hora'], '%H:%M:%S')
            turno.save()

            estudio.estado = Estado.objects.filter(detalle="5").first()
            estudio.save()

            return redirect('/estudios')
        else:
            return render(request, 'estudio/turno.html', {"form": form, "estudio": estudio})
    else:
        form = TurnoForm()

        return render(request, 'estudio/turno.html', {"form": form, "estudio": estudio})


def BuscarTurnoPorFecha(request, id):
    horarios = [('09:00:00', '09:00:00'), ('09:15:00', '09:15:00'), ('09:30:00', '09:30:00'), ('09:45:00', '09:45:00'), ('10:00:00', '10:00:00'), ('10:15:00', '10:15:00'), ('10:30:00', '10:30:00'),
                ('10:45:00', '10:45:00'), ('11:00:00', '11:00:00'), ('11:15:00', '11:15:00'), ('11:30:00', '11:30:00'), ('11:45:00', '11:45:00'), ('12:00:00', '12:00:00'), ('12:15:00', '12:15:00'), ('12:30:00', '12:30:00'), ('12:45:00', '12:45:00'), ('13:00:00', '13:00:00')]
   
    estudio = Estudio.objects.filter(id=id).first()
    if request.method == 'POST':
        formF = TurnoFechaForm(request.POST)
        if formF.is_valid():
            turnos_fecha = Turno.objects.filter(fecha=request.POST['fecha'])

            for turno in turnos_fecha:
                horarios.remove((str(turno.hora), str(turno.hora)))
           
            form = TurnoForm(horarios)
            form.fields['fecha'].initial = request.POST['fecha']
            return render(request, 'estudio/turno.html', {"form": form, "estudio": estudio})
        else:
            return render(request, 'estudio/buscar_turno.html', {"form": formF, "estudio": estudio})
    else:
        form = TurnoFechaForm()

        return render(request, 'estudio/buscar_turno.html', {"form": form, "estudio": estudio})

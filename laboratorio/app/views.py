from django import template
from django.conf.urls import url
from django.forms.forms import Form
from django.http import FileResponse
from django.shortcuts import redirect, render, HttpResponseRedirect, HttpResponse
from django.template import loader
from django.urls.conf import path
from django.template.loader import get_template
from django.contrib import messages
from reportlab.lib.enums import TA_CENTER


from .models import Comprobante, Consentimiento, ConsentimientoFirmado, Lote, MedicoInformante, Muestra, Paciente, ObraSocial, MedicoDerivante, TipoEstudio, Empleado, Estudio, Historial, Estado, Turno, Interpretacion, Patologia

from .forms import EstudioForm, InterpretacionForm, LoginForm, MuestraForm, PacienteForm, HistorialForm, ComprobanteForm, ConsentimientoForm, RMuestraForm, TurnoFechaForm, TurnoForm
import random
import os
from laboratorio import settings
from datetime import date, datetime
from django.core.files.storage import Storage

import io
import pdfkit

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


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


def nuevo_estudio(request):
    if request.method == 'POST':
        form = EstudioForm(request.POST)
        if form.is_valid():
            try:
                estudio = Estudio()
                estudio.presupuesto = request.POST['presupuesto']
                # Deberia ser el empleado que esta en la session actualmente
                estudio.empleadoCarga = Empleado.objects.filter(id=1).first()
                estudio.fechaAlta = datetime.today()
                estudio.medicoDerivante = MedicoDerivante.objects.filter(
                    id=request.POST['medicoDerivante']).first()
                estudio.patologia = Patologia.objects.filter(
                    id=request.POST['patologia']).first()
                estudio.estado = Estado.objects.all().first()
                estudio.tipoEstudio = TipoEstudio.objects.filter(
                    id=request.POST['tipoEstudio']).first()
                estudio.paciente = Paciente.objects.filter(
                    id=request.POST['paciente']).first()
                estudio.save()
                messages.success(request, '!Estudio creado con éxito!')
            except:
                messages.error(request, 'Error! No se pudo crear el estudio')
        return redirect('/estudios')
    else:
        form = EstudioForm()
        return render(request, 'estudio/create.html', {'form': form})


def editar_estudio(request, id):
    if request.method == 'POST':
        try:
            estudio = Estudio.objects.filter(id=id).first()
            estudio.medicoDerivante = MedicoDerivante.objects.get(
                id=request.POST['medicoDerivante'])
            estudio.presupuesto = request.POST['presupuesto']
            estudio.tipoEstudio = TipoEstudio.objects.get(
                id=request.POST['tipoEstudio'])
            estudio.patologia = Patologia.objects.filter(
                id=request.POST['patologia']).first()
            estudio.save()
            messages.success(request, '!Estudio editado con éxito!')
        except:
            messages.error(request, 'Error! No se pudo editar el estudio')
        return redirect('/estudios')
    else:
        estudio = Estudio.objects.get(id=id)
        initial_dict = {
            'presupuesto': estudio.presupuesto,
            'patologia': estudio.patologia,
            'medicoDerivante': estudio.medicoDerivante,
            'tipoEstudio': estudio.tipoEstudio
        }
        form = EstudioForm(initial_dict)
        return render(request, 'estudio/edit.html', {'form': form, 'id': id})


def pacientes(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            # guardar en la BD
            try:
                paciente = Paciente()
                paciente.nombre = request.POST['nombre']
                paciente.apellido = request.POST['apellido']
                paciente.dni = request.POST['dni']
                paciente.telefono = request.POST['telefono']
                paciente.obraSocial = ObraSocial.objects.filter(
                    id=request.POST['obraSocial']).first()
                paciente.numeroAfiliado = random.randrange(99999)
                paciente.save()
                messages.success(request, '!Paciente creado con éxito!')
            except:
                messages.error(request, 'Error! No se pudo crear el paciente')
        return redirect('/pacientes')
    else:
        form = PacienteForm()
        pacientes = Paciente.objects.all()
        return render(request, "pacientes/index.html", {"pacientes": pacientes})


def nuevo_paciente(request):
    obras = ObraSocial.objects.all()
    return render(request, 'pacientes/create.html', {"obras": obras})


def eliminar_paciente(request, id):
    try:
        paciente = Paciente.objects.get(id=id)
        paciente.delete()
        messages.success(request, '¡Paciente borrado con éxito!')
    except:
        messages.error(request, '¡No se puede borrar al paciente!')

    return redirect('/pacientes')


def editar_paciente(request, id):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            # guardar en la BD
            try:
                paciente = Paciente.objects.get(id=request.POST['id'])
                paciente.nombre = request.POST['nombre']
                paciente.apellido = request.POST['apellido']
                paciente.telefono = request.POST['telefono']
                paciente.dni = request.POST['dni']

                obraSocial = ObraSocial.objects.filter(
                    id=request.POST['obraSocial']).first()
                paciente.obraSocial = obraSocial
                paciente.save()
                messages.success(request, '!Paciente editado con éxito!')
            except:
                messages.error(request, 'Error! No se pudo editar al paciente')
            return redirect('/pacientes')
    else:
        form = PacienteForm()
        paciente = Paciente.objects.get(id=id)
        obras = ObraSocial.objects.all()
        return render(request, "pacientes/editar.html", {"obras": obras, "paciente": paciente})


def empleados(request):
    return HttpResponse('Empleados')


# def pendientes(request):
#     return HttpResponse('Pendientes')


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


def nuevo_historial(request, id):
    paciente = Paciente.objects.filter(id=id).first()
    return render(request, "historial/create.html", {"paciente": paciente})


def historial_paciente(request, id):
    paciente = Paciente.objects.filter(id=id).first()
    historial = Historial.objects.filter(paciente_id=paciente.id)
    return render(request, 'historial/index.html', {"paciente": paciente, "historial": historial})

# ------Pendientes---------


def pendientes(request):
    estudiosPendientes = []
    estudiosSinAbonar = Estudio.objects.filter(abonado=False)

    for estudio in estudiosSinAbonar:
        if int(estudio.estado.detalle) > 5:
            estudiosPendientes.append(estudio)
    return render(request, "estudio/pendientes.html", {"estudios": estudiosPendientes})


def pagar_estudios(request):
    abonar = request.POST.getlist('estudios[]')
    try:
        for id in abonar:
            estudio = Estudio.objects.filter(id=id).first()
            estudio.abonado = True
            estudio.save()
        messages.success(request, '¡Se pagaron los estudios con éxito!')
    except:
        messages.error(request, '¡No se pudo realizar el pagos!')


    return redirect('/pendientes')

# ----------------------ESTADOS-----------------------------------------------


def cargar_comprobante(request, id):
    estudio = Estudio.objects.filter(id=id).first()
    if request.method == 'POST':
        form = ComprobanteForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                comprobante = Comprobante()
                comprobante.estudio = estudio
                comprobante.archivo = request.FILES['archivo']
                comprobante.save()
                estudio.estado = Estado.objects.filter(detalle="2").first()
                estudio.save()

                messages.success(request,'!Comprobante cargado con éxito!')
            except:
                messages.error(request, '¡No se pudo cargar el comprobante!')
            return redirect('/estudios')
    else:
        form = ComprobanteForm()

    return render(request, 'estudio/comprobante.html', {"form": form, "estudio": estudio})


def descargar_consentimiento(request, id):
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


def cargar_consentimiento(request, id):
    estudio = Estudio.objects.filter(id=id).first()
    if request.method == 'POST':
        form = ConsentimientoForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                consentimiento = ConsentimientoFirmado()
                consentimiento.estudio = estudio
                consentimiento.archivo = request.FILES['archivo']
                consentimiento.save()
                estudio.estado = Estado.objects.filter(detalle="4").first()
                estudio.save()
                messages.success(request,'!Consentimiento cargado con éxito!')
            except:
                messages.error(request, '¡No se pudo cargar el consentimiento!')

        return redirect('/estudios')
    else:
        form = ConsentimientoForm()

    return render(request, 'estudio/consentimiento.html', {"form": form, "estudio": estudio})

# --------------------------------------TURNO-----------------------------------------


def seleccionar_turno(request, id):
    estudio = Estudio.objects.filter(id=id).first()
    # HORARIOS IRIA EN SETTINGS PARA QUE SE REALICEN CAMBIOS EN UN UNICO LUGAR
    horarios = [('09:00:00', '09:00:00'), ('09:15:00', '09:15:00'), ('09:30:00', '09:30:00'), ('09:45:00', '09:45:00'), ('10:00:00', '10:00:00'), ('10:15:00', '10:15:00'), ('10:30:00', '10:30:00'),
                ('10:45:00', '10:45:00'), ('11:00:00', '11:00:00'), ('11:15:00', '11:15:00'), ('11:30:00', '11:30:00'), ('11:45:00', '11:45:00'), ('12:00:00', '12:00:00'), ('12:15:00', '12:15:00'), ('12:30:00', '12:30:00'), ('12:45:00', '12:45:00'), ('13:00:00', '13:00:00')]

    if request.method == 'POST':

        form = TurnoForm(horarios, request.POST)
        if form.is_valid():
            try:
                turno = Turno()
                turno.estudio = estudio
                turno.fecha = request.POST['fecha']
                turno.hora = datetime.strptime(request.POST['hora'], '%H:%M:%S')
                turno.save()

                estudio.estado = Estado.objects.filter(detalle="5").first()
                estudio.save()
                messages.success(request,'!Se selecciono el turno con éxito!')
            except:
                messages.error(request, '¡No se pudo guardar el turno!')

            return redirect('/estudios')
        else:
            return render(request, 'estudio/turno.html', {"form": form, "estudio": estudio})
    else:
        form = TurnoForm()

        return render(request, 'estudio/turno.html', {"form": form, "estudio": estudio})


def buscar_turno_por_fecha(request, id):
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

# --------------------------------------MUESTRA-----------------------------------------


def cargar_muestra(request, id):
    estudio = Estudio.objects.filter(id=id).first()

    if request.method == 'POST':
        form = MuestraForm(request.POST)

        if form.is_valid():
            try:
                muestra = Muestra()
                muestra.numeroFreezer = request.POST['nroFreezer']
                muestra.mlExtraidos = request.POST['mlExtraidos']
                muestra.fecha = datetime.now()
                muestra.estudio = estudio
                muestra.save()

                estudio.estado = Estado.objects.filter(detalle="6").first()
                estudio.save()
                messages.success(request,'!Muestra cargada con éxito!')
            except:
                messages.error(request, '¡No se pudo cargar la muestra!')

            return redirect('/estudios')
        else:
            return render(request, 'estudio/muestra.html', {"form": form, "estudio": estudio})
    else:
        form = MuestraForm()
        return render(request, 'estudio/muestra.html', {"form": form, "estudio": estudio})


def retiro_muestra(request, id):
    estudio = Estudio.objects.filter(id=id).first()

    if request.method == 'POST':
        form = RMuestraForm(request.POST)

        if form.is_valid():
            try:
                personaRetiro = '{0} {1}'.format(
                    request.POST['nombre'], request.POST['apellido'])
                Muestra.objects.filter(estudio=estudio).update(
                    personaRetira=personaRetiro)
                estudio.estado = Estado.objects.filter(detalle="7").first()
                estudio.save()
                total_muestras = Muestra.objects.exclude(personaRetira=None)
                if total_muestras.count() % 10 == 0:
                    crear_lote()
                    messages.success(request, '¡Se ha creado un lote con éxito!')
                messages.success(request,'!Retiro de muestra cargado con éxito!')
            except:
                messages.error(request, '¡No se pudo cargar el retiro de la muestra!')

            return redirect('/estudios')
        else:
            return render(request, 'estudio/retiro_muestra.html', {"form": form, "estudio": estudio})
    else:
        form = RMuestraForm()
        return render(request, 'estudio/retiro_muestra.html', {"form": form, "estudio": estudio})

# --------------------------------------LOTE-----------------------------------------


def crear_lote():
    lote = Lote()
    lote.save()
    Muestra.objects.filter(lote=None).update(lote=lote)


def lotes(request):
    lotes = Lote.objects.all()
    return render(request, 'lote/index.html', {'lotes': lotes})


def finalizar_proceso(request, id):
    lote = Lote.objects.filter(id=id)
    lote.update(estado='Procesado')
    muestras = Muestra.objects.filter(lote=id)

    for muestra in muestras:
        Estudio.objects.filter(id=muestra.estudio.id).update(estado="8")

    return redirect('/estudios')


def listar_muestras(request, id):
    muestras = Muestra.objects.filter(lote=id)

    return render(request, 'lote/lista_muestras.html', {'muestras': muestras, 'id': id})

# -----------------------------------RESULTADOS--------------------------------------------


def cargar_interpretacion(request, id):
    estudio = Estudio.objects.filter(id=id).first()

    if request.method == 'POST':
        form = InterpretacionForm(request.POST)

        if form.is_valid():
            try:
                interpretacion = Interpretacion()
                interpretacion.resultado = request.POST['resultado']
                interpretacion.medico = MedicoInformante.objects.filter(
                    id=request.POST['medico']).first()
                interpretacion.informe = request.POST['informe']
                interpretacion.fecha = datetime.now()
                interpretacion.estudio = estudio
                interpretacion.save()

                estudio.estado = Estado.objects.filter(detalle="9").first()
                estudio.save()

                messages.success(request, '¡Se ha cargado con éxito la interpretación!')
            except:
                messages.error(request, 'No se pudo cargar la interpretación')
        return redirect('/estudios')
    else:
        form = InterpretacionForm()
        return render(request, 'estudio/interpretacion.html', {'form': form, 'id': id})


def descargar_estudio(request, id):

    interpretacion = Interpretacion.objects.filter(estudio=id).first()
    messages.success(
        request, '¡Descarga Exitosa!')

    return report(request, interpretacion)


def report(request, inter):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = "attachment; filename=Interpretacion_{0}_{1}.pdf".format(
        inter.estudio.id, inter.estudio.tipoEstudio)

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.setLineWidth(.3)
    c.setFont('Helvetica', 25)
    c.drawString(30, 755, 'Laboratorio')

    c.setFont('Helvetica', 12)
    c.drawString(30, 735, 'Interpretación de estudio')

    c.setFont('Helvetica', 15)
    c.drawString(490, 755, 'Fecha')

    c.setFont('Helvetica', 12)
    c.drawString(480, 735, inter.fecha.strftime('%d/%m/%Y'))

    c.setFont('Helvetica', 12)
    c.drawString(30, 650, 'Médico Informante: {0}'.format(inter.medico.nombre))

    c.setFont('Helvetica', 12)
    c.drawString(30, 680, 'Resultado: {0}'.format(inter.resultado))
    c.line(20, 720, 570, 720)

    texto = c.beginText(35, 600)
    texto.setFont('Helvetica', 12)

    texto.textLines(inter.informe)
    c.drawText(texto)

    c.showPage()

    c.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response


def resultado_entregado(request, id):
    estudio = Estudio.objects.filter(id=id).first()

    estudio.estado = Estado.objects.filter(detalle="10").first()
    estudio.save()

    messages.success(request, '¡Estudio {0} finalizado!'.format(estudio.id))
    return redirect('/estudios')

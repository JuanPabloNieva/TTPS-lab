from django.contrib.messages.api import error
from django.shortcuts import redirect, render, HttpResponse
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from .models import Comprobante, Consentimiento, ConsentimientoFirmado, Lote, MedicoInformante, Turno, Interpretacion, Patologia, Muestra, Paciente, ObraSocial, MedicoDerivante, TipoEstudio, Empleado, Estudio, Historial, Estado, Configuracion
from .forms import ConfirmAccountForm, EstudioForm, InterpretacionForm, LoginForm, MuestraForm, PacienteForm, HistorialForm, ComprobanteForm, ConsentimientoForm, RMuestraForm, TurnoFechaForm, TurnoForm, LoginFormPacientes
from laboratorio import settings
from datetime import date, datetime, timedelta
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from dateutil.relativedelta import relativedelta
from django.core.mail import send_mail, EmailMessage



from plotly.offline import plot
import plotly.graph_objects as go
import io, random, os

email = EmailMessage(
    "Laboratorio registro",
    "Felicitaciones se ha registrado",
    "ale1988valdez@gmail.com",
    ['ale.v_1988@hotmail.com'],
    reply_to=['ale.v_1988@hotmail.com']
)

def checkeos_session_permisos(request):
    user = request.session.get('user_id')

    if not user:
        raise PermissionDenied

    return None

def home(request):
    form = LoginForm()
    return redirect('/login', {'form': form})

def login(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                empleado = Empleado.objects.get(usuario=request.POST['usuario'])
                if empleado.password == request.POST['password']:
                    request.session['user_id'] = empleado.id
                    actualizar_estudios_retrasados()
                    messages.success(request, '¡Bienvenido {0}!'.format(empleado.nombre))
                else:
                    messages.error(request, '¡Contraseña invalida!'.format(empleado.nombre))
                    return render(request, 'login.html', {'form': form})
            except:
                messages.error(request, '¡Usuario invalido!')
                return render(request, 'login.html', {'form': form})
            return redirect('/estudios')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

def login_paciente(request):
    if request.POST:
        print(request.POST)
        form = LoginFormPacientes(request.POST)
        if form.is_valid():
            try:
                paciente = Paciente.objects.get(dni=request.POST['dni'])
                print(paciente.new)
                if paciente.new:
                    request.session['user_id'] = paciente.id
                    return redirect('/pacientes/confirmar_password')
                if paciente.password == request.POST['password']:
                    request.session['user_id'] = paciente.id
                    actualizar_estudios_retrasados()
                    messages.success(request, '¡Bienvenido {0}!'.format(paciente.nombre))
                else:
                    messages.error(request, '¡Contraseña invalida!'.format(paciente.nombre))
                    return render(request, 'pacientes/login.html', {'form': form})
            except Exception as e:
                print(e)
                messages.error(request, '¡Usuario invalido!')
                return render(request, 'pacientes/login.html', {'form': form})
            return redirect('/estudios_paciente')
    else:
        form = LoginFormPacientes()
        return render(request, 'pacientes/login.html', {'form': form})

def confirmar_password(request):
     form = ConfirmAccountForm()
     return render(request, 'pacientes/confirmPassword.html', {'form':form})

def check_new_password(request):
    id_paciente = request.session['user_id']
    form = ConfirmAccountForm()  
    paciente = Paciente.objects.get(id=id_paciente)
    if paciente:
        if paciente.password == request.POST['password_actual']:
            if request.POST['password_nuevo'] == request.POST['password_nuevo_rep']:
                paciente.new = False
                paciente.password = request.POST['password_nuevo']
                paciente.save()
                messages.success(request, 'Contraseña Cambiada con exito!')
                return render(request, 'pacientes/estudios.html')
            else:
                messages.error(request, 'Los password nuevo no coinciden')
                return render(request, 'pacientes/confirmPassword.html', {'form':form})
        else:
            messages.error(request, 'La contraseña actual ingresada no es valida')
            return render(request, 'pacientes/confirmPassword.html', {'form':form})
    else:
        messages.error(request, 'Disculpe, hubo un error con el usuario pruebe iniciar sesión de nuevo')
        del request.session['user_id']
        request.session.flush()
        form = LoginFormPacientes()
        return render(request, 'pacientes/login.html', {'form': form})
    


def actualizar_estudios_retrasados():
    ahora = date.today()
    tres_meses = (ahora -relativedelta(months=3))
    tdias = (ahora - timedelta(days=30))
    estudios = Estudio.objects.filter(fechaAlta__lte=tres_meses)
    Estudio.objects.filter(estado="1").filter(fechaAlta__lte=tdias).update(estado="11")

    for estudio in estudios:
        estudio.retrasado = True
        estudio.save()


def logout(request):
    checkeos_session_permisos(request)
    try:
        del request.session['user_id']
        request.session.flush()
    except KeyError:
        pass
    messages.success(request, 'Sesión Finalizada')
    return redirect('/')

def estudios(request):
    checkeos_session_permisos(request)
    estudios = Estudio.objects.all()
    conf = Configuracion.objects.all().first()
    return render(request, 'estudio/index.html', {'estudios': estudios, 'conf': conf})

def estudios_paciente(request):
    id_paciente = request.session['user_id']
    estudios = Estudio.objects.filter(paciente=id_paciente)
    return render(request, 'pacientes/estudios.html', {'estudios': estudios})

def nuevo_estudio(request):
    checkeos_session_permisos(request)
    if request.method == 'POST':
        form = EstudioForm(request.POST)
        if form.is_valid():
            try:
                estudio = Estudio()
                estudio.presupuesto = request.POST['presupuesto']
                estudio.empleadoCarga = Empleado.objects.filter(id=request.session['user_id']).first()
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
                messages.success(request, '¡Estudio creado con éxito!')
            except:
                messages.error(request, 'Error! No se pudo crear el estudio')
        return redirect('/estudios')
    else:
        form = EstudioForm()
        return render(request, 'estudio/create.html', {'form': form})


def editar_estudio(request, id):
    checkeos_session_permisos(request)
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
            messages.success(request, '¡Estudio editado con éxito!')
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


def checkEdad(valor):
    return valor

def pacientes(request):
    #checkeos_session_permisos(request)
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        print(form.is_valid())
        print(request.POST)
        #if form.is_valid():
        if True:
            # guardar en la BD
            try:
                paciente = Paciente()
                paciente.nombre = request.POST['nombre']
                paciente.apellido = request.POST['apellido']
                paciente.telefono = request.POST['telefono']
                paciente.obraSocial = ObraSocial.objects.filter(
                    id=request.POST['obraSocial']).first()
                paciente.numeroAfiliado = random.randrange(99999)
                paciente.password = request.POST['password']
                paciente.email = request.POST['email']
                existe = Paciente.objects.filter(dni=request.POST['dni']).first()
                if existe:
                    messages.error(request, 'El dni ingresado ya se encuentra registrado en el sistema')
                else:
                    paciente.dni = request.POST['dni']
                try:
                    paciente.nombreTutor = request.POST['nombreTutor']
                    paciente.apellidoTutor = request.POST['apellidoTutor']
                except:
                    print('es mayor')
                paciente.fechaNacimiento = request.POST['fechaNacimiento']
                #paciente.save()
                try:
                    email.send()
                except Exception as e:
                    print(e)
                    messages.error(request, 'Paciente creado. Error al enviar email')
                messages.success(request, '¡Paciente creado con éxito!')
            except:
                messages.error(request, 'Error! No se pudo crear el paciente')
        user = request.session.get('user_id')
        if not user:
            return redirect('/login')
        else:
            return redirect('/pacientes')
    else:
        form = PacienteForm()
        pacientes = Paciente.objects.all()
        return render(request, "pacientes/index.html", {"pacientes": pacientes})


def nuevo_paciente(request):
    #checkeos_session_permisos(request)
    obras = ObraSocial.objects.all()
    form = PacienteForm()
    return render(request, 'pacientes/create.html', {"obras": obras, 'form': form})


def eliminar_paciente(request, id):
    checkeos_session_permisos(request)
    try:
        paciente = Paciente.objects.get(id=id)
        paciente.delete()
        messages.success(request, '¡Paciente borrado con éxito!')
    except:
        messages.error(request, '¡No se puede borrar al paciente!')

    return redirect('/pacientes')


def editar_paciente(request, id):
    checkeos_session_permisos(request)
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
                messages.success(request, '¡Paciente editado con éxito!')
            except:
                messages.error(request, 'Error! No se pudo editar al paciente')
            return redirect('/pacientes')
    else:
        form = PacienteForm()
        paciente = Paciente.objects.get(id=id)
        obras = ObraSocial.objects.all()
        return render(request, "pacientes/editar.html", {"obras": obras, "paciente": paciente})


def empleados(request):
    checkeos_session_permisos(request)
    return HttpResponse('Empleados')


# def pendientes(request):
#     return HttpResponse('Pendientes')

# --------HISTORIAL----------


def historial(request):
    checkeos_session_permisos(request)
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
    checkeos_session_permisos(request)
    paciente = Paciente.objects.filter(id=id).first()
    return render(request, "historial/create.html", {"paciente": paciente})


def historial_paciente(request, id):
    checkeos_session_permisos(request)
    paciente = Paciente.objects.filter(id=id).first()
    historial = Historial.objects.filter(paciente_id=paciente.id)
    return render(request, 'historial/index.html', {"paciente": paciente, "historial": historial})

# ------Pendientes---------


def pendientes(request):
    checkeos_session_permisos(request)
    estudiosPendientes = []
    estudiosSinAbonar = Estudio.objects.filter(abonado=False)

    for estudio in estudiosSinAbonar:
        if int(estudio.estado.detalle) > 5:
            estudiosPendientes.append(estudio)
    return render(request, "estudio/pendientes.html", {"estudios": estudiosPendientes})


def pagar_estudios(request):
    checkeos_session_permisos(request)
    abonar = request.POST.getlist('estudios[]')
    try:
        for id in abonar:
            estudio = Estudio.objects.filter(id=id).first()
            estudio.abonado = True
            estudio.save()
        if abonar:
            messages.success(request, '¡Se pagaron los estudios con éxito!')
        else:
            messages.warning(request, '¡Debe seleccionar al menos un checkbox!')
    except:
        messages.error(request, '¡No se pudo realizar el pagos!')


    return redirect('/pendientes')

# ----------------------ESTADOS-----------------------------------------------


def cargar_comprobante(request, id):
    checkeos_session_permisos(request)
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

                messages.success(request,'¡Comprobante cargado con éxito!')
            except:
                messages.error(request, '¡No se pudo cargar el comprobante!')
            return redirect('/estudios')
    else:
        form = ComprobanteForm()

    return render(request, 'estudio/comprobante.html', {"form": form, "estudio": estudio})


def descargar_consentimiento(request, id):
    checkeos_session_permisos(request)
    estudio = Estudio.objects.filter(id=id).first()
    consentimiento = Consentimiento.objects.filter(
        tipoEstudio=estudio.tipoEstudio).first()
    file_path = os.path.join(settings.MEDIA_ROOT, consentimiento.archivo.name)
    # if os.path.exists(file_path):
    #     with open(file_path, 'rb') as fh:
    #         response = HttpResponse(fh.read(), content_type="application/pdf")
    #         response['Content-Disposition'] = 'attachment; filename={0}'.format(\
    #             os.path.basename(file_path))
    #         estudio.estado = Estado.objects.filter(detalle="3").first()
    #         estudio.save()
    #     return response
    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/pdf")
        response['Content-Disposition'] = 'attachment; filename={0}'.format(\
            os.path.basename(file_path))
        estudio.estado = Estado.objects.filter(detalle="3").first()
        estudio.save()
    return response


def cargar_consentimiento(request, id):
    checkeos_session_permisos(request)
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
                messages.success(request,'¡Consentimiento cargado con éxito!')
            except:
                messages.error(request, '¡No se pudo cargar el consentimiento!')

        return redirect('/estudios')
    else:
        form = ConsentimientoForm()

    return render(request, 'estudio/consentimiento.html', {"form": form, "estudio": estudio})

# --------------------------------------TURNO-----------------------------------------


def seleccionar_turno(request, id):
    checkeos_session_permisos(request)
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
                messages.success(request,'¡Se selecciono el turno con éxito!')
            except:
                messages.error(request, '¡No se pudo guardar el turno!')

            return redirect('/estudios')
        else:
            messages.error(request, '¡Los datos ingresados no son válidos!')
            return render(request, 'estudio/turno.html', {"form": form, "estudio": estudio})
    else:
        form = TurnoForm()

        return render(request, 'estudio/turno.html', {"form": form, "estudio": estudio})


def buscar_turno_por_fecha(request, id):
    checkeos_session_permisos(request)
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
    checkeos_session_permisos(request)
    estudio = Estudio.objects.filter(id=id).first()

    if request.method == 'POST':
        form = MuestraForm(request.POST)

        if form.is_valid():
            try:
                turno = Turno.objects.get(estudio=estudio)
                #Si se quiere cargar la muestra antes del turno
                if turno.fecha > date.today():
                    messages.warning(request, 'El paciente tiene turno para la fecha %s'%turno.fecha)
                    return redirect('/estudios')
                muestra = Muestra()
                muestra.numeroFreezer = request.POST['nroFreezer']
                muestra.mlExtraidos = request.POST['mlExtraidos']
                muestra.fechaAlta = datetime.now()
                muestra.estudio = estudio
                muestra.save()

                estudio.estado = Estado.objects.filter(detalle="6").first()
                estudio.save()
                messages.success(request,'¡Muestra cargada con éxito!')
            except:
                messages.error(request, '¡No se pudo cargar la muestra!')

            return redirect('/estudios')
        else:
            return render(request, 'estudio/muestra.html', {"form": form, "estudio": estudio})
    else:
        form = MuestraForm()
        return render(request, 'estudio/muestra.html', {"form": form, "estudio": estudio})


def retiro_muestra(request, id):
    checkeos_session_permisos(request)
    estudio = Estudio.objects.filter(id=id).first()

    if request.method == 'POST':
        form = RMuestraForm(request.POST)

        if form.is_valid():
            try:
                muestra = Muestra.objects.get(estudio=estudio)
                ahora = date.today()
                #Si pasaron 30 dias la muestra se vencio
                if muestra.fechaAlta <= (ahora - timedelta(days=30)):
                    messages.warning(request, '¡La muestra venció! El paciente debe sacar un nuevo turno para la extracción.')
                    Turno.objects.filter(estudio=estudio).delete()
                    muestra.delete()
                    estudio.estado = Estado.objects.filter(detalle="4").first()
                    estudio.save()
                    return redirect('/estudios')
                
                personaRetiro = '{0} {1}'.format(
                    request.POST['nombre'], request.POST['apellido'])
                Muestra.objects.filter(estudio=estudio).update(
                    personaRetira=personaRetiro, fechaRetiro=date.today())
                
                estudio.estado = Estado.objects.filter(detalle="7").first()
                estudio.save()
                total_muestras = Muestra.objects.exclude(personaRetira=None)
                if total_muestras.count() % 10 == 0:
                    crear_lote()
                    messages.success(request, '¡Se ha creado un lote con éxito!')
                messages.success(request,'¡Retiro de muestra cargado con éxito!')
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
    Muestra.objects.filter(lote=None).exclude(personaRetira=None).update(lote=lote)


def lotes(request):
    checkeos_session_permisos(request)
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
    checkeos_session_permisos(request)
    muestras = Muestra.objects.filter(lote=id)

    return render(request, 'lote/lista_muestras.html', {'muestras': muestras, 'id': id})

# -----------------------------------RESULTADOS--------------------------------------------


def cargar_interpretacion(request, id):
    checkeos_session_permisos(request)
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
    checkeos_session_permisos(request)
    interpretacion = Interpretacion.objects.filter(estudio=id).first()
    messages.success(
        request, '¡Descarga Exitosa!')

    return report(request, interpretacion)


def report(request, inter):
    checkeos_session_permisos(request)
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
    checkeos_session_permisos(request)
    estudio = Estudio.objects.filter(id=id).first()
    estudio.fechaFin = datetime.now()
    estudio.estado = Estado.objects.filter(detalle="10").first()
    estudio.save()

    messages.success(request, '¡Estudio {0} finalizado!'.format(estudio.id))
    return redirect('/estudios')
    
    for id in abonar:
        estudio = Estudio.objects.filter(id=id).first()
        estudio.abonado = True
        estudio.save() 

  
    return redirect('/pendientes')


#------Graficos---------
def graficos(request):
    checkeos_session_permisos(request)
    return render(request, "graficos/index.html")

def cantXTipo(request):
    checkeos_session_permisos(request)
    """ 
    View demonstrating how to display a graph object
    on a web page with Plotly. 
    """
    #Me traigo todos los tipos

    tiposDeEstudios = TipoEstudio.objects.all()

    type=[]
    x = []
    y = []
    estudios = Estudio.objects.values_list('tipoEstudio_id')

    
    for tipo in tiposDeEstudios:
        count=0
        type.append(tipo.nombre)
        x.append(tipo.id)
        for estudio in estudios:
            if(estudio[0]==tipo.id):
                count=count+1
        y.append(count)
            
    # List of graph objects for figure.
    # Each object will contain on series of data.
    graphs = []

    # Adding linear plot of y1 vs. x.
    #graphs.append(
    #    go.Scatter(x=x, y=y1, mode='lines', name='Line y1')
    #)

    # Adding scatter plot of y2 vs. x. 
    # Size of markers defined by y2 value.
    #graphs.append(
    #    go.Scatter(x=x, y=y2, mode='markers', opacity=0.8, 
    #               marker_size=y2, name='Scatter y2')
    #)

    # Adding bar plot of y3 vs x.
    
    graphs.append(
        go.Bar(x=x, y=y, name='Cantidad por tipo de estudio') 
    )

    # Setting layout of the figure.
    layout = {
        'title': 'Cantidad de Estudios por Tipo',
        'xaxis_title': 'Tipo de Estudio ',
        'yaxis_title': 'Cantidad',
        'height': 420,
        'width': 560
    }

    # Getting HTML needed to render the plot.
    plot_div = plot({'data': graphs, 'layout': layout}, 
                    output_type='div')
    return render(request,"graficos/cantXTipo.html", {'plot_div': plot_div, 'tiposDeEstudios':tiposDeEstudios})

def cantXMes(request):
    checkeos_session_permisos(request)
    """ 
    View demonstrating how to display a graph object
    on a web page with Plotly. 
    """
    #Me traigo todos los tipos

    month=['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    x = [0,0,0,0,0,0,0,0,0,0,0,0]
    y = [0,0,0,0,0,0,0,0,0,0,0,0]
    estudios = Estudio.objects.all()
    
    for estudio in estudios:
        y[estudio.fechaAlta.month-1]= y[estudio.fechaAlta.month-1] + 1
            
    graphs = []
    
    graphs.append(
        go.Bar(x=month, y=y, name='Cantidad por tipo de estudio') 
    )

    # Setting layout of the figure.
    layout = {
        'xaxis_title': 'Mes',
        'yaxis_title': 'Cantidad',
        'height': 640,
        'width': 900
    }

    # Getting HTML needed to render the plot.
    plot_div = plot({'data': graphs, 'layout': layout}, 
                    output_type='div')
    return render(request,"graficos/cantXMes.html", {'plot_div': plot_div})

def boxplot(request):
    checkeos_session_permisos(request)
    y = []
    estudios = Estudio.objects.filter(estado='10')
    
    filtro=[]
    for estudio in estudios:
        filtro.append({'estudio':estudio, 'muestra': Muestra.objects.filter(estudio=estudio).first()})
    
    for elem in filtro:
        # ejemplo 
        fechaFin = elem['estudio'].fechaFin.strftime("%Y-%m-%d")
        fin = datetime.strptime(fechaFin, '%Y-%m-%d')
        fechaInicio = elem['muestra'].fechaAlta.strftime("%Y-%m-%d")
        inicio =  datetime.strptime(fechaInicio, '%Y-%m-%d')
        
        y.append((fin - inicio).days)

    graphs = []
    
    graphs.append(
        go.Box( y=y, name="Días")
    )

    # Setting layout of the figure.
    layout = {
        'xaxis_title': 'Tiempo promedio de demora ',
        'yaxis_title': 'Cantidad de Días',
        'height': 640,
        'width': 900
    }

    # Getting HTML needed to render the plot.
    plot_div = plot({'data': graphs, 'layout': layout}, 
                    output_type='div')

    return render(request,"graficos/boxplot.html",  {'plot_div': plot_div})

from django.shortcuts import redirect, render, HttpResponseRedirect, HttpResponse
from django.urls.conf import path
from .models import Muestra, Paciente, ObraSocial, MedicoDerivante, TipoEstudio, Empleado, Estudio, Historial, Estado
from django.template.loader import get_template
from .forms import EstudioForm, LoginForm, PacienteForm, HistorialForm
import random
from datetime import date, datetime, timedelta

from plotly.offline import plot
import plotly.graph_objects as go
#import plotly.express as px

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

#--------HISTORIAL----------
def historial(request):
    if request.method == 'POST':
        print(request.POST)
        form = HistorialForm(request.POST)
        print(form)
        if form.is_valid():
            #guardar en la BD
            paciente = Paciente.objects.filter(id=request.POST['paciente']).first()
            detalle = request.POST['texto']
            historial = Historial.objects.create(paciente=paciente, texto=detalle, fecha=datetime.now())
            id=paciente.id
            return  redirect('/historial/paciente/'+str(id))
        else:
            error = "datos invalidos"
    else:
        form = HistorialForm()
    pacientes = Paciente.objects.all()
    return render(request, "historial/create.html", {"pacientes":pacientes, "error": error})

def nuevoHistorial(request,id):
    paciente = Paciente.objects.filter(id=id).first()
    return render(request, "historial/create.html", {"paciente":paciente})

def historialPaciente(request, id):
    paciente = Paciente.objects.filter(id=id).first()
    historial = Historial.objects.filter(paciente_id=paciente.id)
    return render(request, 'historial/index.html', {"paciente":paciente, "historial":historial})

#------Pendientes---------
def pendientes(request):
    estudiosPendientes = []
    estudiosSinAbonar = Estudio.objects.filter(abonado=False)
    is_valid = lambda estudio : estudio.estado.id > 7

    for estudio in estudiosSinAbonar:
        if is_valid(estudio):
            estudiosPendientes.append(estudio)
    return render(request, "estudio/pendientes.html", {"estudios":estudiosPendientes})

def pagarEstudios(request):
    print(request.POST)
    abonar = request.POST.getlist('estudios[]')
    
    for id in abonar:
        estudio = Estudio.objects.filter(id=id).first()
        estudio.abonado = True
        estudio.save() 

  
    return redirect('/pendientes')


#------Graficos---------
def graficos(request):
    return render(request, "graficos/index.html")

def cantXTipo(request):
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
        'xaxis_title': 'Tipo de Estudio ',
        'yaxis_title': 'Cantidad',
        'height': 640,
        'width': 900
    }

    # Getting HTML needed to render the plot.
    plot_div = plot({'data': graphs, 'layout': layout}, 
                    output_type='div')
    return render(request,"graficos/cantXMes.html", {'plot_div': plot_div})

def boxplot(request):
   
    y = []
    estudios = Estudio.objects.all()
    muestras = Muestra.objects.all()

    filtro=[]
    for estudio in estudios:
        for muestra in muestras:
            if muestra.paciente.id == estudio.paciente.id:
                filtro.append({"estudio":estudio, "muestra":muestra})

    # Tenes que tomar la fecha fin del estudio y hacer lo 
    # que hago con fecha de inicio. Y mete estas lineas
    # dentro del for
    fechaFin = datetime.now().strftime("%Y-%m-%d")
    fin = datetime.strptime(fechaFin, '%Y-%m-%d')
    #-------------------------------------------------
    
    for elem in filtro:
        # ejemplo 
        # fechaFin = elem['estudio'].fechaFin.strftime("%Y-%m-%d")
        # fin = datetime.strptime(fechaFin, '%Y-%m-%d')
        fechaInicio = elem['muestra'].fecha.strftime("%Y-%m-%d")
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

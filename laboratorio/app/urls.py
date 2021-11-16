from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='Home'),
    path('estudios', views.estudios, name='Estudios'),
    path('estudios/nuevo', views.nuevoEstudio, name='Crear_Estudio'),
    path('estudios/pendientes', views.pendientes, name='Pendientes'),
    path('pagar', views.pagarEstudios, name="Pagar"),
    path('pacientes', views.pacientes, name='Pacientes'),
    path('pacientes/nuevo', views.nuevoPaciente, name='Registrar Paciente'),
    path('pacientes/eliminar/<id>', views.eliminarPaciente),
    path('pacientes/editar/<id>', views.editarPaciente),
    path('historial', views.historial, name='Historial'),
    path('historial/nuevo/<id>',views.nuevoHistorial, name="Agregar Historial"),
    path('historial/paciente/<id>', views.historialPaciente),
    path('empleados', views.empleados, name='Empleados'),
    path('pendientes', views.pendientes, name='Pendientes'),
    path('login', views.login, name='Login'),
    path('graficos', views.graficos, name="Graficos"),
    path('graficos/cantidadPorTipo', views.cantXTipo, name="Graficos_Tipo"),
    path('graficos/cantidadPorMes', views.cantXMes, name="Graficos_Mes"),
    path('graficos/tiempoDeDemora', views.boxplot, name="Graficos_Boxplot")
]
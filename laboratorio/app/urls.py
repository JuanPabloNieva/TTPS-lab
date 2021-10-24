from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='Home'),
    path('estudios', views.estudios, name='Estudios'),
    path('estudios/nuevo', views.nuevoEstudio, name='Crear_Estudio'),
    path('pacientes', views.pacientes, name='Pacientes'),
    path('pacientes/nuevo', views.nuevoPaciente, name='Registrar Paciente'),
    path('pacientes/eliminar/<id>', views.eliminarPaciente),
    path('pacientes/editar/<id>', views.editarPaciente),
    path('empleados', views.empleados, name='Empleados'),
    path('pendientes', views.pendientes, name='Pendientes'),
    path('login', views.login, name='Login')
]
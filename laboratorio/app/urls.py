from os import name
from django.urls import path


from . import views

urlpatterns = [
    path('', views.home, name='Home'),
    path('estudios', views.estudios, name='Estudios'),
    path('estudios/nuevo', views.nuevoEstudio, name='Crear_Estudio'),
    path('estudios/editar/<id>', views.editarEstudio, name='Editar_Estudio'),
    path('estudios/pendientes', views.pendientes, name='Pendientes'),
    path('estudios/cargar_comprobante/<id>',
         views.CargarComprobante, name='Cargar_Comprobante'),
    path('estudios/descargar_consentimiento/<id>',
         views.DescargarConsentimiento, name='Descargar_Consentimiento'),
    path('estudios/cargar_consentimiento/<id>', views.CargarConsentimiento, name='Cargar_Consentimiento'),
    path('estudios/turno/<id>', views.SeleccionarTurno, name='Seleccionar_Turno'),
    path('estudios/turno/buscar/<id>', views.BuscarTurnoPorFecha, name='Buscar_Turno'),
    path('pagar', views.pagarEstudios, name="Pagar"),
    path('pacientes', views.pacientes, name='Pacientes'),
    path('pacientes/nuevo', views.nuevoPaciente, name='Registrar Paciente'),
    path('pacientes/eliminar/<id>', views.eliminarPaciente),
    path('pacientes/editar/<id>', views.editarPaciente),
    path('historial', views.historial, name='Historial'),
    path('historial/nuevo/<id>', views.nuevoHistorial, name="Agregar Historial"),
    path('historial/paciente/<id>', views.historialPaciente),
    path('empleados', views.empleados, name='Empleados'),
    path('pendientes', views.pendientes, name='Pendientes'),
    path('login', views.login, name='Login')
]

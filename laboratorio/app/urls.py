from django.urls import path

from app import views

urlpatterns = [
    path('', views.home, name='Home'),
    path('estudios', views.estudios, name='Estudios'),
    path('pacientes', views.pacientes, name='Pacientes'),
    path('empleados', views.empleados, name='Empleados'),
    path('pendientes', views.pendientes, name='Pendientes'),
]
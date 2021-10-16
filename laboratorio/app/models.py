from django.db import models

# Create your models here.
class Estudio(models.Model):
    id = models.AutoField(primary_key=True)
    paciente = models.ForeignKey('Paciente', on_delete=models.RESTRICT)
    medicoDerivante = models.ForeignKey('MedicoDerivante', on_delete=models.RESTRICT)
    empleadoCarga = models.ForeignKey('Empleado', on_delete=models.RESTRICT)
    tipoEstudio = models.CharField(max_length=100)
    Estado = models.CharField(max_length=100)
    fechaAlta = models.DateField()
    presupuesto = models.DecimalField(decimal_places=2, max_digits=5)
    diagnosticoPresuntivo = models.TextField(max_length=400)
    

class Paciente(models.Model):
    id = models.AutoField(primary_key=True)
    obraSocial = models.ForeignKey('ObraSocial', on_delete=models.RESTRICT)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.IntegerField()
    telefono = models.IntegerField()
    resumenHClinica = models.TextField(max_length=100)
    numeroAfiliado = models.IntegerField()

class Empleado(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    usuario = models.CharField(max_length=100)
    contraseña = models.CharField(max_length=100)

class MedicoDerivante(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    matricula = models.CharField(max_length=100)
    telefono = models.BigIntegerField()

class ObraSocial(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    telefono = models.IntegerField()
    
class Muestra(models.Model):
    id = models.AutoField(primary_key=True)
    lote = models.ForeignKey('Lote', on_delete=models.RESTRICT)
    paciente = models.ForeignKey('Paciente', on_delete=models.RESTRICT)
    fecha = models.DateField()
    numeroFreezer = models.IntegerField()
    personaRetira = models.CharField(max_length=100)

class Turno(models.Model):
    id = models.AutoField(primary_key=True)
    paciente = models.ForeignKey('Paciente', on_delete=models.RESTRICT)
    fecha = models.DateField()
    hora = models.TimeField()

class Factura(models.Model):
    id = models.AutoField(primary_key=True)
    paciente = models.ForeignKey('Paciente', on_delete=models.RESTRICT)
    estudio = models.ForeignKey('Estudio', on_delete=models.RESTRICT)
    fecha = models.DateField()
    monto = models.IntegerField()

class Lote(models.Model):
    id = models.AutoField(primary_key=True)

class Historial(models.Model):
    id = models.AutoField(primary_key=True)
    paciente = models.ForeignKey('Paciente', on_delete=models.RESTRICT)
    texto = models.CharField(max_length=200)
    fecha = models.DateField()

class Movimiento(models.Model):
    id = models.AutoField(primary_key=True)
    empleado = models.ForeignKey('Empleado', on_delete=models.RESTRICT)
    fecha = models.DateField()
    hora = models.TimeField()
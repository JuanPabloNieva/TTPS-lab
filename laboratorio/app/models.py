from django.db import models

# Create your models here.
class Estudio(models.Model):
    id = models.AutoField(primary_key=True)
    paciente = models.ForeignKey('Paciente', on_delete=models.RESTRICT)
    medicoDerivante = models.ForeignKey('MedicoDerivante', on_delete=models.RESTRICT)
    empleadoCarga = models.ForeignKey('Empleado', on_delete=models.RESTRICT)
    tipoEstudio = models.ForeignKey('TipoEstudio', on_delete=models.RESTRICT)
    estado = models.CharField(max_length=100)
    abonado = models.BooleanField(null=False, default=False)
    fechaAlta = models.DateField()
    presupuesto = models.DecimalField(decimal_places=2, max_digits=19)
    diagnosticoPresuntivo = models.TextField(max_length=400)
    
class TipoEstudio(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return u'{0}'.format(self.nombre)

class Paciente(models.Model):
    id = models.AutoField(primary_key=True)
    obraSocial = models.ForeignKey('ObraSocial', on_delete=models.RESTRICT)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.BigIntegerField()
    telefono = models.BigIntegerField()
    resumenHClinica = models.TextField(max_length=100)
    numeroAfiliado = models.BigIntegerField()

    def __str__(self):
        return u'{0} {1} ({2})'.format(self.nombre, self.apellido, self.dni)

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

    def __str__(self):
        return u'{0} {1}'.format(self.nombre, self.apellido)

class ObraSocial(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    telefono = models.BigIntegerField()
    
class Muestra(models.Model):
    id = models.AutoField(primary_key=True)
    lote = models.ForeignKey('Lote', on_delete=models.RESTRICT)
    paciente = models.ForeignKey('Paciente', on_delete=models.RESTRICT)
    fecha = models.DateField()
    numeroFreezer = models.BigIntegerField()
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
    monto = models.FloatField()

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
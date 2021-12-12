from django.db import models
from django.db.models.fields import DateField
from django.db.models.fields.related import ForeignKey

# Create your models here.


class Estudio(models.Model):
    id = models.AutoField(primary_key=True)
    paciente = models.ForeignKey('Paciente', on_delete=models.RESTRICT)
    medicoDerivante = models.ForeignKey(
        'MedicoDerivante', on_delete=models.RESTRICT)
    empleadoCarga = models.ForeignKey('Empleado', on_delete=models.RESTRICT)
    tipoEstudio = models.ForeignKey('TipoEstudio', on_delete=models.RESTRICT)
    estado = models.ForeignKey('Estado', on_delete=models.DO_NOTHING)
    abonado = models.BooleanField(null=False, default=False)
    fechaAlta = models.DateField()
    presupuesto = models.DecimalField(decimal_places=2, max_digits=19)
    patologia = models.ForeignKey('Patologia', on_delete=models.RESTRICT)
    fechaFin = models.DateField(null=True)
    retrasado = models.BooleanField(default=False)


class TipoEstudio(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return u'{0}'.format(self.nombre)


class Paciente(models.Model):
    id = models.AutoField(primary_key=True)
    obraSocial = models.ForeignKey('ObraSocial', on_delete=models.RESTRICT, null=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    nombreTutor = models.CharField(max_length=100, null=True)
    apellidoTutor = models.CharField(max_length=100, null=True)
    dni = models.BigIntegerField()
    telefono = models.BigIntegerField()
    email = models.TextField(max_length=100)
    numeroAfiliado = models.BigIntegerField()
    fechaNacimiento =  models.DateField()
    password = models.CharField(max_length=100)
    new = models.BooleanField(default=True)

    def __str__(self):
        return u'{0} {1} ({2})'.format(self.nombre, self.apellido, self.dni)


class Empleado(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    usuario = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return u'{0} {1}'.format(self.nombre, self.apellido)


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
    lote = models.ForeignKey('Lote', on_delete=models.RESTRICT, null=True)
    estudio = models.ForeignKey('Estudio', on_delete=models.RESTRICT)
    fechaAlta = models.DateField()
    fechaRetiro = models.DateField(null=True)
    numeroFreezer = models.BigIntegerField()
    mlExtraidos = models.DecimalField(decimal_places=1, max_digits=3)
    personaRetira = models.CharField(max_length=100, null=True)


class Turno(models.Model):
    id = models.AutoField(primary_key=True)
    estudio = models.ForeignKey('Estudio', on_delete=models.RESTRICT)
    fecha = models.DateField()
    hora = models.TimeField()


class Factura(models.Model):
    id = models.AutoField(primary_key=True)
    estudio = models.ForeignKey('Estudio', on_delete=models.RESTRICT)
    fecha = models.DateField()
    monto = models.FloatField()


class Lote(models.Model):
    id = models.AutoField(primary_key=True)
    estado = models.CharField(default='En procesamiento', max_length=50)


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


class Estado(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    detalle = models.CharField(max_length=300)

    def __str__(self):
        return '{0}-{1}'.format(self.nombre, self.detalle)


class Comprobante(models.Model):
    id = models.AutoField(primary_key=True)
    estudio = models.ForeignKey('Estudio', on_delete=models.RESTRICT)
    archivo = models.FileField(upload_to='comprobantes/')


class Consentimiento(models.Model):
    id = models.AutoField(primary_key=True)
    tipoEstudio = models.ForeignKey('TipoEstudio', on_delete=models.RESTRICT)
    archivo = models.FileField(upload_to='consentimientos/')

    def __str__(self):
        return '{0}'.format(self.tipoEstudio)


class ConsentimientoFirmado(models.Model):
    id = models.AutoField(primary_key=True)
    estudio = models.ForeignKey('Estudio', on_delete=models.RESTRICT)
    archivo = models.FileField(upload_to='consentimientosFirmados/')

    def __str__(self):
        return '{0}'.format(self.tipoEstudio)


class Interpretacion(models.Model):
    estudio = models.OneToOneField(
        Estudio, on_delete=models.CASCADE, primary_key=True)
    resultado = models.CharField(max_length=20)
    fecha = models.DateField()
    medico = models.ForeignKey('MedicoInformante', on_delete=models.RESTRICT)
    informe = models.CharField(max_length=10000)

class MedicoInformante(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)

    def __str__(self):
        return '{0} {1}'.format(self.nombre, self.apellido)

class Patologia(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return '{0}'.format(self.nombre)
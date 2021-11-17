import datetime
from django import forms
from django.forms.widgets import DateInput, FileInput, Select
from app.models import Paciente, MedicoDerivante, TipoEstudio, MedicoInformante, Patologia
from datetime import date


class LoginForm(forms.Form):
    usuario = forms.CharField(label='Nombre de usuario', widget=forms.TextInput(
        attrs={'class': 'form-control'}), required=True)
    password = forms.CharField(
        label='Contraseña', required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class EstudioForm(forms.Form):
    presupuesto = forms.DecimalField(label='Presupuesto', min_value=0, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Presupuesto'}), required=True)
    patologia = forms.ModelChoiceField(queryset=Patologia.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control', 'id': 'patologias'}), label='Diagnostico Presuntivo', required=True, to_field_name='id', empty_label='--Seleccionar--')
    paciente = forms.ModelChoiceField(queryset=Paciente.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control', 'id': 'pacientes'}), label='Paciente', required=True, to_field_name='id', empty_label='--Seleccionar--')
    medicoDerivante = forms.ModelChoiceField(queryset=MedicoDerivante.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control'}), label='Médico Derivante', required=True, to_field_name='id', empty_label='--Seleccionar--')
    tipoEstudio = forms.ModelChoiceField(queryset=TipoEstudio.objects.all(), label='Tipo de Estudio', widget=forms.Select(
        attrs={'class': 'form-control'}), empty_label='--Seleccionar--', to_field_name='id', required=True)


class PacienteForm(forms.Form):
    nombre = forms.CharField(label='Nombre', required=True)
    apellido = forms.CharField(label='Apelldio', required=True)
    dni = forms.IntegerField(
        label='DNI', help_text='Ingrese DNI sin puntos', required=True)
    telefono = forms.CharField(label='Telefono', required=True)
    obraSocial = forms.IntegerField(label='Obra Social')


class HistorialForm(forms.Form):
    paciente = forms.IntegerField(label='Paciente', required=True)
    texto = forms.CharField(label='Detalles', widget=forms.Textarea,
                            min_length=0, max_length=400, required=True)


class ComprobanteForm(forms.Form):
    archivo = forms.FileField(label='Comprobante de pago', widget=FileInput(
        attrs={'accept': 'application/pdf'}))


class ConsentimientoForm(forms.Form):
    archivo = forms.FileField(label='Consentimiento firmado por el paciente', widget=FileInput(
        attrs={'accept': 'application/pdf'}))


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class TurnoForm(forms.Form):
    fecha = forms.DateField(label='Fecha', widget=DateInput(
        attrs={'readonly': 'readonly', 'class': 'form-control w-50'}), required=True)
    hora = forms.ChoiceField(label='Hora', widget=Select(
        attrs={'class': 'form-control w-50'}), required=True)

    def __init__(self, choices, *args, **kwargs):
        super(TurnoForm, self).__init__(*args, **kwargs)
        self.fields['hora'].choices = choices


class TurnoFechaForm(forms.Form):

    fecha = forms.DateField(label='Fecha', widget=DateInput(
        attrs={'class': 'form-control w-50'}), required=True)

    def clean_fecha(self):
        data = self.cleaned_data['fecha']

        if data < datetime.date.today():
            raise forms.ValidationError(
                ('Fecha Invalida - No puede sacar un turno para una fecha pasada'))

        if date(data.year, data.month, data.day).weekday() == 5 or date(data.year, data.month, data.day).weekday() == 6:
            raise forms.ValidationError(
                ('Fecha Invalida - Los turnos se dan unicamente de Lunes a Viernes'))

        return data


class MuestraForm(forms.Form):
    nroFreezer = forms.IntegerField(label='Número de freezer', widget=forms.NumberInput(
        attrs={'class': 'form-control w-50 mb-3'}), min_value=0)
    mlExtraidos = forms.DecimalField(
        label='Mililitros Extraidos', decimal_places=1, max_digits=3, max_value=12.5, min_value=5, widget=forms.NumberInput(attrs={'class': 'form-control w-50 mb-2'}))


class RMuestraForm(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=50, min_length=1,
                             widget=forms.TextInput(attrs={'class': 'form-control w-50 mb-3'}))
    apellido = forms.CharField(label='Apellido', max_length=50, min_length=1,
                               widget=forms.TextInput(attrs={'class': 'form-control w-50 mb-3'}))


class InterpretacionForm(forms.Form):
    choices = [(
        'POSITIVO', 'POSITIVO'), ('NEGATIVO', 'NEGATIVO')]
    resultado = forms.ChoiceField(label='Resultado', choices=choices, widget=forms.Select(
        attrs={'class': 'form-control'}), required=True)
    medico = forms.ModelChoiceField(queryset=MedicoInformante.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control', 'id': 'medicos'}), label='Médico', required=True, to_field_name='id', empty_label='--Seleccionar--')
    informe = forms.CharField(label='Informe', widget=forms.Textarea(
        attrs={'class': 'form-control', 'style': 'resize:none; overflow:stroll; width:65%', 'placeholder': 'Ingrese el informe', 'rows': '6', 'cols': '10', 'wrap': 'hard'}), min_length=0, max_length=10000, required=True)

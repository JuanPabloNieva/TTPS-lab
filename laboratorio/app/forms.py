from django import forms
from app.models import Paciente, MedicoDerivante, TipoEstudio


class LoginForm(forms.Form):
    usuario = forms.CharField(label='Nombre de usuario', widget=forms.TextInput(
        attrs={'class': 'form-control'}), required=True)
    password = forms.CharField(
        label='Contraseña', required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class EstudioForm(forms.Form):
    presupuesto = forms.DecimalField(label='Presupuesto', min_value=0, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Presupuesto'}), required=True)
    diagnosticoPresuntivo = forms.CharField(label='Diagnostico Presuntivo', widget=forms.Textarea(
        attrs={'class': 'form-control', 'style': 'resize:none; overflow:stroll;', 'placeholder': 'Ingrese el diagnostico presuntivo'}), min_length=0, max_length=400, required=True)
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
    obraSocial = forms.IntegerField(label='Obra Social', required=True)

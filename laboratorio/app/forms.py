from django import forms
from app.models import Paciente, MedicoDerivante

class LoginForm(forms.Form):
    usuario = forms.CharField(label='Nombre de usuario', required=True)
    password = forms.CharField(label='Contraseña', required=True, widget=forms.PasswordInput)

class EstudioForm(forms.Form):
    presupuesto = forms.FloatField(label='Presupuesto',min_value=0, required=True)
    diagnosticoPresuntivo = forms.CharField(label='Diagnostico Presuntivo', widget=forms.Textarea, min_length=0, max_length=400, required=True)
    paciente = forms.ModelChoiceField(queryset=Paciente.objects.distinct('nombre'), required=True)
    medicoDerivante = forms.ModelChoiceField(queryset=MedicoDerivante.objects.distinct('nombre'), required=True)
    tipoEstudio = forms.CharField(max_length=100, required=True)


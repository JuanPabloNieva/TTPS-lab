from django.contrib import admin

from app.models import Empleado, MedicoDerivante, TipoEstudio, ObraSocial, Estado, Consentimiento
# Register your models here.

admin.site.register(Empleado)
admin.site.register(MedicoDerivante)
admin.site.register(TipoEstudio)
admin.site.register(ObraSocial)
admin.site.register(Estado)
admin.site.register(Consentimiento)
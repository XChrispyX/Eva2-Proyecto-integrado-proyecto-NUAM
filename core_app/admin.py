from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Rol, Usuario, CalificacionTributaria, DeclaracionJurada, Factor, LogSeguridad

admin.site.register(Rol)
admin.site.register(Usuario)
admin.site.register(CalificacionTributaria)
admin.site.register(DeclaracionJurada)
admin.site.register(Factor)
admin.site.register(LogSeguridad)

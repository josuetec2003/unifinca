from django.contrib import admin

from .models import Modulo, Sala, Estado, Estadio, CicloLarva, DatosLarva, DatoParametroAgua

admin.site.register(Estado)
admin.site.register(Estadio)


@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'departamento',)

@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
	list_display = ('modulo', 'nombre',)
	ordering = ('modulo', 'nombre')

@admin.register(CicloLarva)
class CicloLarvaAdmin(admin.ModelAdmin):
	list_display = ('numero_ciclo', 'sala', 'poblacion_inicial', 'fecha_inicio', 'fecha_final', 'estado')

@admin.register(DatosLarva)
class MedidaLarvaAdmin(admin.ModelAdmin):
	list_display = [f.name for f in DatosLarva._meta.fields]

@admin.register(DatoParametroAgua)
class DatoParametroAguaAdmin(admin.ModelAdmin):
	list_display = [f.name for f in DatoParametroAgua._meta.fields]

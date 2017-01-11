from django.contrib import admin

from .models import OrigenAgua, Microbiologia, ModelTest


admin.site.register(OrigenAgua)


@admin.register(ModelTest)
class ModelTestAdmin(admin.ModelAdmin):
	list_display = [f.name for f in ModelTest._meta.fields]

@admin.register(Microbiologia)
class MicrobiologiaAdmin(admin.ModelAdmin):
	list_display = [f.name for f in Microbiologia._meta.fields]

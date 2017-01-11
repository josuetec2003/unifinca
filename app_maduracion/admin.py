from django.contrib import admin
from .models import Maduracion

@admin.register(Maduracion)
class MaduracionAdmin(admin.ModelAdmin):
	list_display = [f.name for f in Maduracion._meta.fields]


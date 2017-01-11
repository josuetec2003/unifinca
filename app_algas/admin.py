from django.contrib import admin
from .models import Alga

@admin.register(Alga)
class AlgaAdmin(admin.ModelAdmin):
	list_display = ('total_algas', 'fecha', 'tw', 'cm', 'nv')


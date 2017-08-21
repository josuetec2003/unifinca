from django.contrib import admin
from .models import Alga

@admin.register(Alga)
class AlgaAdmin(admin.ModelAdmin):
	list_display = ('fecha', 'tw', 'cm', 'nv', 't')


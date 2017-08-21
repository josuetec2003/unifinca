from __future__ import unicode_literals

from app_larvarios.models import Sala
from django.db import models

class Maduracion(models.Model):
	sala = models.ForeignKey(Sala)
	copula = models.PositiveIntegerField(null=True, blank=True)
	ovas = models.PositiveIntegerField(null=True, blank=True)
	nauplio = models.PositiveIntegerField(null=True, blank=True)
	nauplios_hembra = models.PositiveIntegerField(null=True, blank=True, verbose_name='Nauplios/Hembra')
	factura_nauplios = models.PositiveIntegerField(null=True, blank=True)
	descarte = models.PositiveIntegerField(null=True, blank=True)
	fecha = models.DateField(auto_now_add=True)

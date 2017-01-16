from __future__ import unicode_literals

from app_larvarios.models import Sala
from django.db import models

class Maduracion(models.Model):
	sala = models.ForeignKey(Sala)
	copula = models.IntegerField(null=True, blank=True)
	ovas = models.IntegerField(null=True, blank=True)
	nauplio = models.IntegerField(null=True, blank=True)
	factura_nauplios = models.IntegerField(null=True, blank=True)
	descarte = models.IntegerField(null=True, blank=True)
	fecha = models.DateField(auto_now_add=True)

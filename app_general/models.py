#coding: utf8
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class OrigenAgua(models.Model):
	nombre = models.CharField(max_length=40)

	def __str__(self):
		return self.nombre

@python_2_unicode_compatible
class Microbiologia(models.Model):
	origen_agua = models.ForeignKey(OrigenAgua)
	departamento = models.CharField(max_length=15)
	ufc = models.IntegerField(verbose_name='UFC/ml')
	fecha = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.ufc)

class DatoParametroAgua(models.Model):
	origen_agua = models.ForeignKey(OrigenAgua)
	departamento = models.CharField(max_length=15)
	fecha_ingreso = models.DateTimeField(auto_now_add=True)
	ph = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='pH')
	temperatura = models.DecimalField(max_digits=5, decimal_places=2)
	oxigeno = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	salinidad = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

	class Meta:
		ordering = ['-fecha_ingreso', 'departamento']

@python_2_unicode_compatible
class ModelTest(models.Model):
	nombre = models.CharField(max_length=10)
	ph = models.DecimalField(max_digits=6, decimal_places=2)
	temp = models.DecimalField(max_digits=6, decimal_places=2)

	def __str__(self):
		return self.nombre



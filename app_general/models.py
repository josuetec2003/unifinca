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

@python_2_unicode_compatible
class ModelTest(models.Model):
	nombre = models.CharField(max_length=10)
	ph = models.DecimalField(max_digits=6, decimal_places=2)
	temp = models.DecimalField(max_digits=6, decimal_places=2)

	def __str__(self):
		return self.nombre



#coding: utf8
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Modulo(models.Model):
	nombre = models.CharField(max_length=10)
	departamento = models.CharField(max_length=15, null=True)

	def __str__(self):
		return '%s > %s' % (self.departamento, self.nombre)


@python_2_unicode_compatible
class Sala(models.Model):
	nombre = models.CharField(max_length=10)
	modulo = models.ForeignKey(Modulo)

	def __str__(self):
		return '%s > %s > %s' % (self.modulo.departamento, self.modulo.nombre, self.nombre)


@python_2_unicode_compatible
class Estado(models.Model):
	estado_ciclo = models.CharField(max_length=15)

	def __str__(self):
		return self.estado_ciclo


@python_2_unicode_compatible
class Estadio(models.Model):
	nombre = models.CharField(max_length=25)

	def __str__(self):
		return self.nombre


@python_2_unicode_compatible
class CicloLarva(models.Model):
	poblacion_inicial = models.PositiveIntegerField(verbose_name='Población inicial')
	fecha_inicio = models.DateTimeField(auto_now_add=True)
	fecha_final = models.DateTimeField(null=True, blank=True)
	numero_ciclo = models.SmallIntegerField(verbose_name='Número de ciclo')
	estado = models.ForeignKey(Estado)
	sala = models.ForeignKey(Sala)

	def __str__(self):
		return 'Ciclo %d [ %s ] > %s (%s)' % (self.numero_ciclo, self.fecha_inicio, self.sala, self.estado.estado_ciclo)


@python_2_unicode_compatible
class MedidaLarva(models.Model):
	fecha = models.DateField(auto_now_add=True)
	numero_dia = models.SmallIntegerField()
	retraso = models.SmallIntegerField(verbose_name='Porcentaje de retraso')
	mortalidad = models.SmallIntegerField(verbose_name='Porcentaje de mortalidad')
	deformidad = models.SmallIntegerField(verbose_name='Porcentaje de deformidad')
	poblacion = models.PositiveIntegerField(verbose_name='Población actual')
	supervivencia = models.SmallIntegerField(verbose_name='Porcentaje de supervivencia', null=True, blank=True)
	estadio = models.ForeignKey(Estadio)
	imm = models.CharField(max_length=25, verbose_name='Índice de masa muscular', null=True, blank=True)
	ciclo_larva = models.ForeignKey(CicloLarva)

	def __str__(self):
		return str(self.numero_dia)

class DatoParametroAgua(models.Model):
	ciclo = models.ForeignKey(CicloLarva)
	fecha_ingreso = models.DateTimeField(auto_now_add=True)
	ph = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='pH')
	temperatura = models.DecimalField(max_digits=5, decimal_places=2)
	oxigeno = models.DecimalField(max_digits=5, decimal_places=2)
	salinidad = models.DecimalField(max_digits=5, decimal_places=2)

	class Meta:
		ordering = ['-fecha_ingreso', 'ciclo']

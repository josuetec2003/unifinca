from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Alga(models.Model):
	tw = models.IntegerField(null=True, blank=True, verbose_name='TW (Thalassiosira weissflogii)')
	cm = models.IntegerField(null=True, blank=True, verbose_name='CM (Chaetoceros muelleri)')
	nv = models.IntegerField(null=True, blank=True, verbose_name='NV (Navicula)')
	fecha = models.DateTimeField(auto_now_add=True)

	def _total_algas(self):
		return self.tw + self.cm + self.nv

	total_algas = property(_total_algas)

	def __str__(self):
		return 'Total de algas: %s' % self.fecha

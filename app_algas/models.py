from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Alga(models.Model):
	tw = models.IntegerField(null=True, blank=True, verbose_name='TW (Thalassiosira weissflogii)', default=0)
	cm = models.IntegerField(null=True, blank=True, verbose_name='CM (Chaetoceros muelleri)', default=0)
	nv = models.IntegerField(null=True, blank=True, verbose_name='NV (Navicula)', default=0)
	t = models.IntegerField(null=True, blank=True, verbose_name='T (Tetraselmis)', default=0)
	fecha = models.DateField(auto_now_add=True)

	# def _total_algas(self):
	# 	return int(self.tw) + int(self.cm) + int(self.nv) + int(self.t)

	# total_algas = property(_total_algas)

	def __str__(self):
		return '{0} {1} {2} {3} {4}'.format(self.fecha, self.tw, self.cm, self.nv, self.t)

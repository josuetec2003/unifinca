#coding: utf8
from django import forms
from .models import CicloLarva, DatoParametroAgua

class CicloLarvaForm(forms.ModelForm):
	class Meta:
		model = CicloLarva
		fields = '__all__'
		#widgets = { 'fecha': forms.HiddenInput() }


class DatoParametroAguaForm(forms.ModelForm):
	class Meta:
		model = DatoParametroAgua
		fields = '__all__'
		widgets = { 'ciclo': forms.HiddenInput() }
#coding: utf8
from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Microbiologia, DatoParametroAgua

class DatoParametroAguaForm(forms.ModelForm):
	class Meta:
		model = DatoParametroAgua
		fields = '__all__'
		widgets = { 'departamento': forms.HiddenInput() }


class MicrobiologiaForm(forms.ModelForm):
	class Meta:
		model = Microbiologia
		fields = '__all__'
		widgets = { 'departamento': forms.HiddenInput() }


class MyAuthenticationForm(AuthenticationForm):
	def __init__(self, *args, **kwargs):
		super(MyAuthenticationForm, self).__init__(*args, **kwargs)

		self.base_fields['username'].widget.attrs['class'] = 'validate'
		self.base_fields['username'].widget.attrs['placeholder'] = 'Nombre de usuario'

		self.base_fields['password'].widget.attrs['class'] = 'validate'
		self.base_fields['password'].widget.attrs['placeholder'] = 'Contraseña'

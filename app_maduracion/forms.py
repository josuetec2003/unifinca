#coding: utf8
from django import forms
from .models import Maduracion

class MaduracionForm(forms.ModelForm):
	class Meta:
		model = Maduracion
		fields = '__all__'
		widgets = { 'sala': forms.HiddenInput() }
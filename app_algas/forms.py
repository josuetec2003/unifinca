#coding: utf8
from django import forms
from .models import Alga

class AlgaForm(forms.ModelForm):
	class Meta:
		model = Alga
		fields = '__all__'
		widgets = { 'fecha': forms.HiddenInput() }
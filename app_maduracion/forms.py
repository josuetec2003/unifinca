#coding: utf8
from django import forms
from .models import Maduracion

class MaduracionForm(forms.ModelForm):
	class Meta:
		model = Maduracion
		fields = '__all__'
		widgets = { 'sala': forms.HiddenInput() }

	def __init__(self, *args, **kwargs):
		super(MaduracionForm, self).__init__(*args, **kwargs)
		self.fields['copula'].widget = forms.TextInput(attrs={'class': 'comma-separated', 'autofocus': 'autofocus'})
		self.fields['ovas'].widget = forms.TextInput(attrs={'class': 'comma-separated',})
		self.fields['nauplio'].widget = forms.TextInput(attrs={'class': 'comma-separated'})
		self.fields['nauplios_hembra'].widget = forms.TextInput(attrs={'class': 'comma-separated'})
		self.fields['factura_nauplios'].widget = forms.TextInput(attrs={'class': 'comma-separated'})
		self.fields['descarte'].widget = forms.TextInput(attrs={'class': 'comma-separated'})

		#self.fields['copula'].widget.attrs.update({'class': 'comma-separated'})
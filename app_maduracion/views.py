#coding: utf8
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings # Para obtener el departamento
from django.contrib.auth.decorators import login_required

from app_general.models import Microbiologia
from app_general.forms import MicrobiologiaForm

from .models import Maduracion
from .forms import MaduracionForm

from datetime import datetime
import json

@login_required()
def index(request):
	depto = settings.DEPARTAMENTOS['m']

	# variables form_micro y consulta van a base.html
	form_micro = MicrobiologiaForm(initial={'departamento': depto})
	consulta = Microbiologia.objects.filter(departamento=depto, fecha__date=datetime.today()).order_by('-fecha')

	form_maduracion = MaduracionForm()
	datos_maduracion = Maduracion.objects.all().order_by('-fecha')

	contexto = {
		'form_micro': form_micro, 
		'depto': depto, 
		'datos_micro': consulta,
		'form_maduracion': form_maduracion,
		'datos_maduracion': datos_maduracion
	}

	return render(request, 'maduracion.html', contexto)



@login_required()
def guardar_datos_maduracion(request):
	if request.method == 'POST':
		form = MaduracionForm(request.POST)

		if form.is_valid():
			ultimo_objeto = form.save()

			tr = '<tr><td>%s</td><td>%d</td><td>%d</td><td>%d</td><td>%d</td><td>%d</td></tr>' % (ultimo_objeto.fecha, ultimo_objeto.copula, ultimo_objeto.ovas, ultimo_objeto.nauplio, ultimo_objeto.descarte, ultimo_objeto.factura_nauplios)
			resultado = {'respuesta': 'Información guardada con éxito', 'fila': tr}
			return HttpResponse(json.dumps(resultado), content_type='application/json')
		else:
			resultado = {'respuesta': 'Error'}
			return JsonResponse(resultado)




















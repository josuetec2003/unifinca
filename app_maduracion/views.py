#coding: utf8
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings # Para obtener el departamento
from django.contrib.auth.decorators import login_required

from app_general.models import Microbiologia, DatoParametroAgua
from app_general.forms import MicrobiologiaForm, DatoParametroAguaForm

from app_larvarios.models import Modulo, Sala

from .models import Maduracion
from .forms import MaduracionForm

from datetime import datetime
import json

@login_required()
def index(request):
	depto = settings.DEPARTAMENTOS['m']

	# variables form_micro y consulta van a base.html
	form_micro = MicrobiologiaForm(initial={'departamento': depto})
	consulta1 = Microbiologia.objects.filter(departamento=depto, fecha__date=datetime.today()).order_by('-fecha')

	form_maduracion = MaduracionForm()
	consulta2 = Maduracion.objects.all().order_by('-fecha')

	# variables form_params y consulta van a base.html
	form_params = DatoParametroAguaForm(initial={'departamento': depto})
	consulta3 = DatoParametroAgua.objects.filter(departamento=depto).order_by('-fecha_ingreso')

	# ciclos y analisis de larvas en salas
	modulos = Modulo.objects.filter(departamento=depto)

	contexto = {
		'form_micro': form_micro, 
		'form_maduracion': form_maduracion,
		'form_params': form_params,
		'depto': depto, 
		'datos_micro': consulta1,
		'datos_maduracion': consulta2,
		'datos_params': consulta3,
		'modulos': modulos
	}

	return render(request, 'maduracion.html', contexto)


@login_required()
def datos_maduracion(request, id):
	try:
		sala = Sala.objects.get(pk=id)
		form = MaduracionForm(initial={'sala': sala})

		consulta = Maduracion.objects.filter(sala=sala).order_by('-id')

		return render(request, 'datos-maduracion.html', {'sala': sala, 'form': form, 'datos_maduracion': consulta})
	except Sala.DoesNotExist:
		return HttpResponse('No existe la sala')


@login_required()
def guardar_datos(request):
	if request.method == 'POST':
		form = MaduracionForm(request.POST)

		if form.is_valid():
			ultimo_objeto = form.save()

			tr = '<tr><td>%s</td><td>%d</td><td>%d</td><td>%d</td><td>%d</td><td>%d</td></tr>' % (ultimo_objeto.fecha, ultimo_objeto.copula, ultimo_objeto.ovas, ultimo_objeto.nauplio, ultimo_objeto.descarte, ultimo_objeto.factura_nauplios)
			resultado = {'respuesta': 'Información guardada con éxito', 'fila': tr}
			return JsonResponse(resultado)
		else:
			resultado = {'respuesta': 'Error'}
			return JsonResponse(resultado)




















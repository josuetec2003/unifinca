#coding: utf8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings # Para obtener el departamento
from django.contrib.auth.decorators import login_required

from .forms import AlgaForm
from .models import Alga

from app_general.models import Microbiologia
from app_general.forms import MicrobiologiaForm

from datetime import datetime, timedelta
import json

@login_required()
def index(request):
	depto = settings.DEPARTAMENTOS['a']

	# datos de los ultimos 30 dias
	ultimo_mes = datetime.today() - timedelta(days=30)
	datos = Alga.objects.filter(fecha__gte=ultimo_mes).order_by('-fecha')
	form_algas = AlgaForm()

	# variables form_micro y consulta van a base.html
	form_micro = MicrobiologiaForm(initial={'departamento': depto})
	consulta = Microbiologia.objects.filter(departamento=depto).order_by('-fecha')

	return render(request, 'algas.html', {'datos_algas': datos, 'form_algas': form_algas, 'form_micro': form_micro, 'depto': depto, 'datos_micro': consulta})


@login_required
def guardar_conteo(request):
	if request.method == "POST":
		form = AlgaForm(data=request.POST)

		if form.is_valid():
			ultimo_objeto = form.save() # save() guarda y devuelve el objeto

			tr = '<tr><td>%s</td><td>%d</td><td>%d</td><td>%d</td><td>%d</td></tr>' % (ultimo_objeto.fecha, ultimo_objeto.tw, ultimo_objeto.cm, ultimo_objeto.nv, ultimo_objeto.total_algas)
				
			resultado = {'ok': True, 'msg': 'Información guardada con éxito', 'fila': tr}
			return JsonResponse(resultado)

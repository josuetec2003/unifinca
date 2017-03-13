#coding: utf8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings # Para obtener el departamento
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .forms import AlgaForm
from .models import Alga

from app_general.models import Microbiologia, DatoParametroAgua, OrigenAgua
from app_general.forms import MicrobiologiaForm, DatoParametroAguaForm

from datetime import datetime, timedelta

@login_required()
def index(request):
	depto = settings.DEPARTAMENTOS['a']

	# datos de los ultimos 30 dias
	#ultimo_mes = datetime.today() - timedelta(days=30)
	consulta1 = Alga.objects.filter(fecha=timezone.now())
	form_algas = AlgaForm()

	# variables form_micro y consulta van a base.html
	form_micro = MicrobiologiaForm(initial={'departamento': depto})
	ultimo_mes = datetime.today() - timedelta(days=30)
	consulta2 = Microbiologia.objects.filter(departamento=depto, fecha__gte=ultimo_mes).order_by('-fecha')

	# variables form_params y consulta van a base.html	
	form_params = DatoParametroAguaForm(initial={'departamento': depto})	
	consulta4 =  OrigenAgua.objects.all()

	contexto = {
		'datos_algas': consulta1,
		'datos_micro': consulta2,
		'form_algas': form_algas, 
		'form_micro': form_micro, 
		'form_params': form_params, 
		'datos_origen_agua': consulta4,
		'depto': depto
	}

	return render(request, 'algas.html', contexto)


@login_required
def guardar_conteo(request):
	if request.method == "POST":
		form = AlgaForm(data=request.POST)

		if form.is_valid():
			ultimo_objeto = form.save() # save() guarda y devuelve el objeto

			tr = '<tr><td>%s</td><td>%d</td><td>%d</td><td>%d</td><td>%d</td></tr>' % (ultimo_objeto.fecha, ultimo_objeto.tw, ultimo_objeto.cm, ultimo_objeto.nv, ultimo_objeto.total_algas)
				
			resultado = {'ok': True, 'msg': 'Información guardada con éxito', 'fila': tr}
			return JsonResponse(resultado)

@login_required()
def filtro(request):

	filtro = request.GET.get('filtro')
	tr = ""

	if filtro == 'hoy':
		datos = Alga.objects.filter(fecha = datetime.today())

		for dato in datos:
			tr += '<tr><th>%s</th><td>%d</td><td>%d</td><td>%d</td></tr>' % (dato.fecha, dato.tw, dato.cm, dato.nv)

	elif filtro == 'mes':
		ultimo_mes = datetime.today() - timedelta(days=30)
		datos = Alga.objects.filter(fecha__gte = ultimo_mes)
		
		for dato in datos:
			tr += '<tr><th>%s</th><td>%d</td><td>%d</td><td>%d</td></tr>' % (dato.fecha, dato.tw, dato.cm, dato.nv)
	else: #rango
		datos = Alga.objects.filter(fecha__range = (request.GET.get('desde'), request.GET.get('hasta')))
		
		for dato in datos:
			tr += '<tr><th>%s</th><td>%d</td><td>%d</td><td>%d</td></tr>' % (dato.fecha, dato.tw, dato.cm, dato.nv)

	return JsonResponse({'respuesta': tr})






#coding: utf8
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings # Para obtener el departamento
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from app_general.models import OrigenAgua, Microbiologia, DatoParametroAgua
from app_general.forms import MicrobiologiaForm, DatoParametroAguaForm

from app_larvarios.models import Modulo, Sala

from .models import Maduracion
from .forms import MaduracionForm

from time import sleep
from datetime import datetime, timedelta
import json

@login_required()
def index(request):
	depto = settings.DEPARTAMENTOS['m']

	# variables form_micro y consulta van a base.html
	form_micro = MicrobiologiaForm(initial={'departamento': depto})
	ultimo_mes = datetime.today() - timedelta(days=30)
	consulta1 = Microbiologia.objects.filter(departamento=depto, fecha__gte=ultimo_mes).order_by('-fecha')

	form_maduracion = MaduracionForm()
	consulta2 = Maduracion.objects.all().order_by('-fecha')

	# variables form_params y consulta van a base.html
	form_params = DatoParametroAguaForm(initial={'departamento': depto})
	#consulta3 = DatoParametroAgua.objects.filter(departamento=depto).order_by('-fecha_ingreso')
	consulta4 =  OrigenAgua.objects.all()

	# ciclos y analisis de larvas en salas
	modulos = Modulo.objects.filter(departamento=depto)

	contexto = {
		'form_micro': form_micro, 
		'form_maduracion': form_maduracion,
		'form_params': form_params,
		'depto': depto, 
		'datos_micro': consulta1,
		'datos_maduracion': consulta2,
		#'datos_params': consulta3,
		'datos_origen_agua': consulta4,
		'modulos': modulos,
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
		# quita el separador de miles (formato string) para insertarlo en campos int
		copula = request.POST.get('copula').replace(",", "")
		ovas = request.POST.get('ovas').replace(",", "")
		nauplio = request.POST.get('nauplio').replace(",", "")
		nauplios_hembra = request.POST.get('nauplios_hembra').replace(",", "")
		factura_nauplios = request.POST.get('factura_nauplios').replace(",", "")
		descarte = request.POST.get('descarte').replace(",", "")


		# deja en cero los campos que fueron dejados en blanco
		copula = 0 if copula == '' else int(copula)
		ovas = 0 if ovas == '' else int(ovas)
		nauplio = 0 if nauplio == '' else int(nauplio)
		nauplios_hembra = 0 if nauplios_hembra == '' else int(nauplios_hembra)
		factura_nauplios = 0 if factura_nauplios == '' else int(factura_nauplios)
		descarte = 0 if descarte == '' else int(descarte)

		if copula == 0 and ovas == 0 and nauplio == 0 and factura_nauplios == 0 and descarte == 0 and nauplios_hembra == 0:
			resultado = {'respuesta': 'El formulario está vacío'}
			return JsonResponse(resultado)
		else:			

			sala = Sala.objects.get(pk=request.POST.get('sala'))

			# se inserta en la BD
			maduracion_obj = Maduracion(copula=copula, ovas=ovas, nauplio=nauplio, nauplios_hembra=nauplios_hembra, factura_nauplios=factura_nauplios, descarte=descarte, sala=sala)

			try:
				maduracion_obj.save()

				# se obtiene el objeto recien insertado
				ultimo_objeto =  Maduracion.objects.last()

				tr = '<tr><td>%s</td><td>%d</td><td>%d</td><td>%d</td><td>%d</td><td>%d</td></tr>' % (ultimo_objeto.fecha, ultimo_objeto.copula, ultimo_objeto.ovas, ultimo_objeto.nauplio, ultimo_objeto.descarte, ultimo_objeto.factura_nauplios)
				resultado = {'respuesta': 'Información guardada con éxito', 'fila': tr}
				return JsonResponse(resultado)

			except Exception as e:
				resultado = {'respuesta': e}
				return JsonResponse(resultado)

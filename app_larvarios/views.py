#coding: utf8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings # Para obtener el departamento
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Sum

from app_general.models import Microbiologia, DatoParametroAgua as DPAG
from app_general.forms import MicrobiologiaForm, DatoParametroAguaForm as DPAForm

from .models import Modulo, Estado, CicloLarva, Sala, DatoParametroAgua
from .forms import CicloLarvaForm, DatoParametroAguaForm

from datetime import datetime
import json

@login_required()
def index(request):
	depto = settings.DEPARTAMENTOS['l']

	# variables form_micro y consulta van a base.html
	form_micro = MicrobiologiaForm(initial={'departamento': depto})
	consulta1 = Microbiologia.objects.filter(departamento=depto, fecha__date=datetime.today()).order_by('-fecha')

	# variables form_params y consulta van a base.html
	form_params = DPAForm(initial={'departamento': depto})
	consulta2 = DPAG.objects.filter(departamento=depto).order_by('-fecha_ingreso')

	# ciclos y analisis de larvas en salas
	modulos = Modulo.objects.filter(departamento=depto)

	# formulario para agregar parametros
	activo = Estado.objects.get(pk=1)
	form_ciclo = CicloLarvaForm(initial={'estado': activo})

	contexto = {
		'form_micro': form_micro,
		'form_ciclo': form_ciclo,
		'form_params': form_params,
		'datos_micro': consulta1,
		'datos_params': consulta2,
		'modulos': modulos,
		'depto': depto, 
	}

	return render(request, 'larvarios.html', contexto)


@login_required()
def nuevo_ciclo(request):
	if request.method == 'POST':
		form = CicloLarvaForm(request.POST)

		if form.is_valid():
			try:
				numero_ciclo = form.cleaned_data['numero_ciclo']
				sala = form.cleaned_data['sala']

				# verificar si existe un ciclo activo para esta sala
				estado_activo = Estado.objects.get(pk=1)
				existe_ciclo = CicloLarva.objects.filter(sala=sala, estado=estado_activo)

				if not existe_ciclo:
					form.save()
					return JsonResponse({'sala_id': sala.id, 'num_ciclo': numero_ciclo, 'respuesta': 'Un nuevo ciclo ha sido iniciado'})
				else:
					return JsonResponse({'respuesta': 'Ciclo %d aun está activo' % existe_ciclo[0].numero_ciclo})
				
			except Exception, e:
				return JsonResponse({'respuesta': e})
		else:
			return HttpResponse(form.errors)


@login_required()
def cerrar_ciclo(request):
	sala = Sala.objects.get(pk=request.GET.get('sala_id'))
	estado_activo = Estado.objects.get(pk=1)
	
	# Model.objects.get(pk=1): Devuelve un objeto del modelo
	# Model.objects.filter(estado='Activo'): Devuelve un queryset. Utilizar [indice] para acceder a los objetos

	ciclo_activo = CicloLarva.objects.filter(sala=sala, estado=estado_activo)
	
	if not ciclo_activo:
		#return HttpResponse('No hay ciclo')
		# No hay ciclo en la sala para cerrar
		return JsonResponse({'respuesta': 'No hay ciclo activo en esta sala'})
	else:

		#return HttpResponse('Hay ciclo')
		# Se cierra el ciclo
		estado_terminado = Estado.objects.get(estado_ciclo='Terminado')
		ciclo_activo[0].estado = estado_terminado
		ciclo_activo[0].fecha_final = datetime.today()
		ciclo_activo[0].save()

		# Aunque solo hay un ciclo activo por sala, se obtiene el objeto con .filter para utilizar 'if not ciclo_activo' ...
		# al verificar que no hay ciclos. En cambio con .get, el operador not no es soportado, en su lugar hay que utilizar Try ...
		# para manejar la excepcion 'matching query does not exist'

		return JsonResponse({'respuesta': 'El ciclo %d ha sido terminado' % ciclo_activo[0].numero_ciclo})


@login_required()
def verificar_ciclo_activo(request):
	sala = Sala.objects.get(pk=request.GET.get('sala_id'))
	estado_activo = Estado.objects.get(pk=1)
	estado_terminado = Estado.objects.get(pk=2)
	
	ciclo = CicloLarva.objects.filter(sala=sala, estado=estado_activo)

	if ciclo: # La sala tiene un ciclo activo
		return JsonResponse({'ok': True, 'num_ciclo': ciclo[0].numero_ciclo, 'class': 'btn-ciclo-activo'})
	else:     # La sala no tiene ciclo activo, se obtendra cual fue el ultimo ciclo
		# select * from ciclolarva where sala = n and estado = 'terminado' order by numero ciclo desc limit 1;
		ultimo_ciclo = CicloLarva.objects.filter(sala=sala, estado=estado_terminado).order_by('-numero_ciclo')[:1]

		if ultimo_ciclo:
			return JsonResponse({'ok': False, 'num_ciclo': ultimo_ciclo[0].numero_ciclo})


@login_required()
def parametros_agua(request, id):	
	try:
		sala = Sala.objects.get(pk=id)
		estado_activo = Estado.objects.get(pk=1)
		ciclo = CicloLarva.objects.get(sala=sala, estado=estado_activo)
		form = DatoParametroAguaForm(initial={'ciclo': ciclo})

		datos_params = DatoParametroAgua.objects.filter(ciclo=ciclo).order_by('-fecha_ingreso')

		return render(request, 'parametros-agua.html', {'sala': sala.nombre, 'form': form, 'id': id, 'datos_params': datos_params})
	except Sala.DoesNotExist:
		return HttpResponse('No existe la sala')
	except CicloLarva.DoesNotExist:
		return HttpResponseRedirect('/larvarios/')


@login_required()
def parametros_agua_guardar(request):
	if request.method == 'POST':
		form = DatoParametroAguaForm(data=request.POST)

		if form.is_valid():
			ultimo_objeto = form.save()

			if request.is_ajax():
				tr = '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (ultimo_objeto.fecha_ingreso, ultimo_objeto.ph, ultimo_objeto.temperatura, ultimo_objeto.oxigeno, ultimo_objeto.salinidad)
					
				resultado = {'respuesta': 'Información guardada con éxito', 'fila': tr}
				return JsonResponse(resultado)
			else:
				return HttpResponseRedirect('/larvarios/')










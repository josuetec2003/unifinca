#coding: utf8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils.html import escape
from django.utils.timezone import datetime 	# para obtener la fecha de hoy con django
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from datetime import datetime, timedelta
import json
from time import sleep

from .models import Microbiologia, DatoParametroAgua, OrigenAgua
from .forms import MicrobiologiaForm, MyAuthenticationForm, DatoParametroAguaForm

@login_required()
def guardar_microbiologia(request):
	
	#if request.is_ajax():
	if request.method == 'POST':
		form = MicrobiologiaForm(data=request.POST)

		if form.is_valid():				
			ultimo_objeto = form.save() # save() guarda y devuelve el objeto

			tr = '<tr><td>%s</td><td>%d</td><td>%s</td></tr>' % (ultimo_objeto.origen_agua.nombre, ultimo_objeto.ufc, ultimo_objeto.fecha)
			
			resultado = {'ok': True, 'msg': 'Información guardada con éxito', 'fila': tr}
			return JsonResponse(resultado)


@login_required()
def guardar_params_agua(request):
	
	#if request.is_ajax():
	if request.method == 'POST':
		form = DatoParametroAguaForm(data=request.POST)
		sleep(3)
		if form.is_valid():				
			ultimo_objeto = form.save() # save() guarda y devuelve el objeto

			tr = '<tr><td>%s</td><td>%s</td><td>%.2f</td><td>%.2f</td><td>%.2f</td><td>%.2f</td></tr>' % (ultimo_objeto.fecha_ingreso, ultimo_objeto.origen_agua, ultimo_objeto.ph, ultimo_objeto.temperatura, ultimo_objeto.oxigeno, ultimo_objeto.salinidad)
			
			resultado = {'respuesta': 'Información guardada con éxito', 'fila': tr}
			return JsonResponse(resultado)


@login_required()
def filtrar_microbiologia(request):
	pass
	# visualizar la informacion de la peticion
	# return HttpResponse(escape(repr(request.POST)))

	# if request.method == 'POST':
	# 	datos = []
	# 	try:
	# 		inicio = datetime.strptime(request.POST.get('fecha-inicio'), '%m-%d-%Y')
	# 		final = datetime.strptime(request.POST.get('fecha-fin'), '%m-%d-%Y')

	# 		# inicio = parse_date(request.POST.get('fecha-inicio'))
	# 		# final = parse_date(request.POST.get('fecha-fin'))

	# 		depto = request.POST.get('deptoid')

	# 		consulta = DatoParametroAgua.objects.filter(departamento=depto, fecha_ingreso__range=(inicio, final))			

	# 		if not consulta:
	# 			t = {'result': '<tr><td colspan="6">No hay datos para mostrar</td></tr>'}
	# 			datos.append(t)
	# 		else: # Hay registros
	# 			for fila in consulta:
	# 				t = {'result': '<tr><td>%s</td><td>%.2f</td><td>%.2f</td><td>%.2f</td><td>%.2f</td></tr>' % (fila.origen_del_agua.nombre, fila.ph, fila.temperatura, fila.oxigeno, fila.salinidad)}
	# 				datos.append(t)

	# 		return HttpResponse(json.dumps(datos), content_type='application/json')
	# 	except Exception, e:
	# 		t = {'result': '<tr><td colspan="6">Error: '+ e +'</td></tr>'}
	# 		datos.append(t)
	# 		return HttpResponse(json.dumps(datos), content_type='application/json')


def form_login(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect('/dashboard/')
	else:
		form = MyAuthenticationForm()
		return render(request, 'login.html', {'form': form})


def validate_login(request):
	if request.method == 'POST':
		form = MyAuthenticationForm(data=request.POST)

		if form.is_valid():
			user = authenticate(username=request.POST.get('username'), 
								password=request.POST.get('password'))

			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect('/dashboard/')
			else:
				return render(request, 'login.html', {'form': form, 'msg': 'Las credenciales no son correctas', 'error': True})
		else:
			return render(request, 'login.html', {'form': form, 'msg': 'Las credenciales no son correctas', 'error': True})
	else:
		return HttpResponseRedirect('/')
		

@login_required()
def sign_off(request):
	logout(request)
	return HttpResponseRedirect('/')

@login_required()
def filtrar_params_agua(request):
	filtro, tr, origen = request.GET.get('filtro'), "", OrigenAgua.objects.get(pk=request.GET.get('fuente'))

	if filtro == 'hoy':
		datos = DatoParametroAgua.objects.filter(departamento = request.GET.get('depto'), origen_agua = origen, fecha_ingreso = datetime.today())

		for dato in datos:
			tr += '<tr><th>%s</th><td>%.2f</td><td>%.2f</td><td>%.2f</td><td>%.2f</td></tr>' % (dato.fecha_ingreso, dato.ph, dato.temperatura, dato.oxigeno, dato.salinidad)

	elif filtro == 'mes':
		ultimo_mes = datetime.today() - timedelta(days=30)
		datos = DatoParametroAgua.objects.filter(departamento = request.GET.get('depto'), origen_agua = origen, fecha_ingreso__gte = ultimo_mes).order_by('fecha_ingreso')
		
		for dato in datos:
			tr += '<tr><th>%s</th><td>%.2f</td><td>%.2f</td><td>%.2f</td><td>%.2f</td></tr>' % (dato.fecha_ingreso, dato.ph, dato.temperatura, dato.oxigeno, dato.salinidad)
	else: #rango
		datos = DatoParametroAgua.objects.filter(departamento = request.GET.get('depto'), origen_agua = origen, fecha_ingreso__range = (request.GET.get('desde'), request.GET.get('hasta'))).order_by('fecha_ingreso')
		
		for dato in datos:
			tr += '<tr><th>%s</th><td>%.2f</td><td>%.2f</td><td>%.2f</td><td>%.2f</td></tr>' % (dato.fecha_ingreso, dato.ph, dato.temperatura, dato.oxigeno, dato.salinidad)

	return JsonResponse({'origen': origen.nombre, 'depto': request.GET.get('depto'), 'respuesta': tr})
















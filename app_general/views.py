#coding: utf8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils.html import escape
from django.utils.timezone import datetime 	# para obtener la fecha de hoy con django
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from datetime import datetime
import json

from .models import Microbiologia
from .forms import MicrobiologiaForm, MyAuthenticationForm

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
















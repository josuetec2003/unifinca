#coding: utf8
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings # Para obtener el departamento
from django.db.models import Avg

from app_larvarios.models import Estado, CicloLarva, DatoParametroAgua, Modulo, Sala
from app_maduracion.models import Maduracion
from app_general.models import Microbiologia, OrigenAgua
from app_algas.models import Alga
from wkhtmltopdf.views import PDFTemplateResponse

from datetime import datetime


def rpt1(request):
	datos_de = request.GET.get('datos_de')
	estado_activo = Estado.objects.get(pk=1)

	desde = request.GET.get('desde')
	hasta = request.GET.get('hasta')

	tr = ""

	if datos_de == 'todo-promedio':
		consulta = CicloLarva.objects.filter(estado=estado_activo).values('sala__nombre','sala__modulo__nombre').annotate(PH=Avg('datoparametroagua__ph'), TEMP=Avg('datoparametroagua__temperatura'), OXI=Avg('datoparametroagua__oxigeno'), SAL=Avg('datoparametroagua__salinidad')).order_by('sala__modulo__nombre')

		tr += u"""
			<thead>
				<tr>
					<th></th>					
					<th>pH</th>
					<th>Temperatura</th>
					<th>Oxígeno</th>
					<th>Salinidad</th>				
				</tr>
			</thead>

			<tbody>
		"""

		for fila in consulta:
			tr += """
				<tr>
					<th>%s %s</th>
					<td>%s</td>
					<td>%s</td>
					<td>%s</td>
					<td>%s</td>
				</tr>
			""" % (fila['sala__modulo__nombre'], fila['sala__nombre'], fila['PH'], fila['TEMP'], fila['OXI'], fila['SAL'])

		tr += '</tbody>'

	elif datos_de == 'todo-diario':

		if desde and hasta:
			consulta = CicloLarva.objects.filter(estado=estado_activo, datoparametroagua__fecha_ingreso__range = (desde, hasta)).values('sala__nombre','sala__modulo__nombre', 'datoparametroagua__ph', 'datoparametroagua__temperatura', 'datoparametroagua__oxigeno', 'datoparametroagua__salinidad', 'datoparametroagua__fecha_ingreso').order_by('sala__nombre','sala__modulo__nombre','datoparametroagua__fecha_ingreso')
		else:
			consulta = CicloLarva.objects.filter(estado=estado_activo).values('sala__nombre','sala__modulo__nombre', 'datoparametroagua__ph', 'datoparametroagua__temperatura', 'datoparametroagua__oxigeno', 'datoparametroagua__salinidad', 'datoparametroagua__fecha_ingreso').order_by('sala__nombre','sala__modulo__nombre','datoparametroagua__fecha_ingreso')

		tr += u"""
			<thead>
				<tr>
					<th></th>					
					<th>pH</th>
					<th>Temperatura</th>
					<th>Oxígeno</th>
					<th>Salinidad</th>
					<th>Fecha</th>			
				</tr>
			</thead>

			<tbody>
		"""

		for fila in consulta:
			tr += """
				<tr>
					<th>%s %s</th>					
					<td>%.2f</td>
					<td>%.2f</td>
					<td>%.2f</td>
					<td>%.2f</td>
					<td>%s</td>					
				</tr>
			""" % (fila['sala__modulo__nombre'], fila['sala__nombre'], fila['datoparametroagua__ph'], fila['datoparametroagua__temperatura'], fila['datoparametroagua__oxigeno'], fila['datoparametroagua__salinidad'], fila['datoparametroagua__fecha_ingreso'])

		tr += '</tbody>'
	else:	

		if desde and hasta:
			consulta = CicloLarva.objects.filter(pk=datos_de, estado=estado_activo, datoparametroagua__fecha_ingreso__range = (desde, hasta)).values('datoparametroagua__fecha_ingreso', 'datoparametroagua__ph', 'datoparametroagua__temperatura', 'datoparametroagua__oxigeno', 'datoparametroagua__salinidad')
		else:
			consulta = CicloLarva.objects.filter(pk=datos_de, estado=estado_activo).values('datoparametroagua__fecha_ingreso', 'datoparametroagua__ph', 'datoparametroagua__temperatura', 'datoparametroagua__oxigeno', 'datoparametroagua__salinidad')
		
		tr += u"""
			<thead>
				<tr>
					<th></th>					
					<th>pH</th>
					<th>Temperatura</th>
					<th>Oxígeno</th>
					<th>Salinidad</th>				
				</tr>
			</thead>

			<tbody>
		"""

		for fila in consulta:
			tr += """
				<tr>
					<th>%s</th>
					<td>%.2f</td>
					<td>%.2f</td>
					<td>%.2f</td>
					<td>%.2f</td>
				</tr>
			""" % (fila['datoparametroagua__fecha_ingreso'], fila['datoparametroagua__ph'], fila['datoparametroagua__temperatura'], fila['datoparametroagua__oxigeno'], fila['datoparametroagua__salinidad'])

		tr += '</tbody>'

	return JsonResponse({'respuesta': tr})



def rpt2(request):
	datos_de = request.GET.get('datos_de')
	sala = Sala.objects.get(pk=datos_de)

	desde = request.GET.get('desde')
	hasta = request.GET.get('hasta')

	tr = ""	

	if desde and hasta:
		consulta = Maduracion.objects.filter(sala=sala, fecha__range=(desde, hasta)).order_by('fecha')
	else:
		consulta = Maduracion.objects.filter(sala=sala).order_by('fecha')

	tr += u"""
		<thead>
			<tr>
				<th></th>					
				<th>Copula</th>
				<th>Ovas</th>
				<th>Nauplio</th>
				<th>Factura</th>
				<th>Descarte</th>				
			</tr>
		</thead>

		<tbody>
	"""

	for fila in consulta:
		tr += """
			<tr>
				<th>%s</th>
				<td>%s</td>
				<td>%s</td>
				<td>%s</td>
				<td>%s</td>
				<td>%s</td>
			</tr>
		""" % (fila.fecha, fila.copula, fila.ovas, fila.nauplio, fila.factura_nauplios, fila.descarte)

	tr += '</tbody>'

	return JsonResponse({'respuesta': tr})


def rpt3(request):
	depto = settings.DEPARTAMENTOS[request.GET.get('depto')]
	muestra = OrigenAgua.objects.get(pk=request.GET.get('muestra'))
	desde = request.GET.get('desde')
	hasta = request.GET.get('hasta')

	tr = ""	

	if desde and hasta:
		consulta = Microbiologia.objects.filter(origen_agua=muestra, departamento=depto, fecha__range=(desde, hasta)).order_by('fecha')
	else:
		consulta = Microbiologia.objects.filter(origen_agua=muestra, departamento=depto).order_by('fecha')

	tr += u"""
		<thead>
			<tr>
				<th></th>					
				<th>UFC/ml</th>							
			</tr>
		</thead>

		<tbody>
	"""
	for fila in consulta:
		tr += """
			<tr>
				<th>%s</th>
				<td>%d</td>				
			</tr>
		""" % (fila.fecha, fila.ufc)

	tr += '</tbody>'

	return JsonResponse({'respuesta': tr})
	


def index(request):
	estado_activo = Estado.objects.get(pk=1)
	ciclos_activos = CicloLarva.objects.filter(estado=estado_activo) # Para CBO de rpt1

	salas_maduracion = Sala.objects.filter(modulo__departamento='Maduración')

	aguas_muestra = OrigenAgua.objects.all()
	return render(request, 'index.html', {'ciclos': ciclos_activos, 'salas_maduracion': salas_maduracion, 'aguas_muestra': aguas_muestra})

@login_required()
def test(request):
	template_name = "pdf-test.html"
	context = {}
	estado_activo = Estado.objects.get(pk=1)
	context['object_list'] = CicloLarva.objects.filter(estado=estado_activo).values('sala__nombre','sala__modulo__nombre').annotate(PH=Avg('datoparametroagua__ph'), TEMP=Avg('datoparametroagua__temperatura'), OXI=Avg('datoparametroagua__oxigeno'), SAL=Avg('datoparametroagua__salinidad')).order_by('sala__modulo__nombre')
	
	response = PDFTemplateResponse(request = request,
									template = template_name,
									filename = "test.pdf",
									context = context,										
									show_content_in_browser = True,
									cmd_options = {'orientation': 'portrait',
													'margin-top': 15, 
													'margin-bottom': 20, 
													'default-header': True, 
													'header-left': 'Listado de parametros en salas con ciclo activo', 
													'footer-line': True})

	return response


@login_required()
def reporte_maduracion(request):
	# datos = Maduracion.objects.select_related()
	# return render(request, 'pdf-maduracion.html', {'object_list': datos})

	var_inicio = request.POST.get('inicio')
	var_final = request.POST.get('final')

	context = {}

	if var_inicio and not var_final:
		# desde fecha inicio
		context['object_list'] = Maduracion.objects.filter(fecha__gte=var_inicio).select_related().order_by('sala')
		context['filter'] = "desde {0}".format(var_inicio)
	elif not var_inicio and var_final:
		# datos hasta la fecha final
		context['object_list'] = Maduracion.objects.filter(fecha__lte=var_final).select_related().order_by('sala')
		context['filter'] = "hasta {0}".format(var_final)
	elif var_inicio and var_final:
		# datos entre el rango de fechas
		context['object_list'] = Maduracion.objects.filter(fecha__range=(var_inicio,var_final)).select_related().order_by('sala')
		context['filter'] = "desde {0} - hasta {1}".format(var_inicio, var_final)
	else:
		# todos los datos
		context['object_list'] = Maduracion.objects.all().order_by('sala')
		context['filter'] = "Todos los registros"


	template_name = "pdf-maduracion.html"	

	response = PDFTemplateResponse(request = request,
									template = template_name,
									filename = "maduracion.pdf",
									context = context,										
									show_content_in_browser = True,
									cmd_options = {'orientation': 'portrait',
													'margin-top': 15, 
													'margin-bottom': 20, 
													'default-header': True, 
													'header-left': u'Reporte de maduración por sala', 
													'footer-line': True})

	return response

@login_required()
def reporte_algas(request):
	var_inicio = request.POST.get('inicio')
	var_final = request.POST.get('final')

	context = {}

	if var_inicio and not var_final:
		# desde fecha inicio
		context['object_list'] = Alga.objects.filter(fecha__gte=var_inicio).select_related().order_by('-fecha')
		context['filter'] = "desde {0}".format(var_inicio)
	elif not var_inicio and var_final:
		# datos hasta la fecha final
		context['object_list'] = Alga.objects.filter(fecha__lte=var_final).select_related().order_by('-fecha')
		context['filter'] = "hasta {0}".format(var_final)
	elif var_inicio and var_final:
		# datos entre el rango de fechas
		context['object_list'] = Alga.objects.filter(fecha__range=(var_inicio,var_final)).select_related().order_by('-fecha')
		context['filter'] = "desde {0} - hasta {1}".format(var_inicio, var_final)
	else:
		# todos los datos
		context['object_list'] = Alga.objects.all().order_by('-fecha')
		context['filter'] = "Todos los registros"


	template_name = "pdf-algas.html"	

	response = PDFTemplateResponse(request = request,
									template = template_name,
									filename = "algas.pdf",
									context = context,										
									show_content_in_browser = True,
									cmd_options = {'orientation': 'portrait',
													'margin-top': 15, 
													'margin-bottom': 20, 
													'default-header': True, 
													'header-left': u'Reporte de algas', 
													'footer-line': True})


	return response



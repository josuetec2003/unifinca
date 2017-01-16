#coding: utf8
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Avg

from app_larvarios.models import Estado, CicloLarva
from app_maduracion.models import Maduracion
from app_algas.models import Alga
from wkhtmltopdf.views import PDFTemplateResponse

from datetime import datetime

@login_required()
def index(request):
	return render(request, 'index.html')

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



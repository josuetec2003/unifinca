from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from app_larvarios.models import Estado, CicloLarva

@login_required()
def dashboard(request):
	estado_activo = Estado.objects.get(pk=1)
	datos = CicloLarva.objects.filter(estado=estado_activo).values('sala__nombre','sala__modulo__nombre').annotate(PH=Avg('datoparametroagua__ph'), TEMP=Avg('datoparametroagua__temperatura'), OXI=Avg('datoparametroagua__oxigeno'), SAL=Avg('datoparametroagua__salinidad')).order_by('sala__modulo__nombre')
	return render(request, 'dashboard.html', {'datos': datos})
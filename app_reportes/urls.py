from django.conf.urls import url
from . import views

# /reporte/

urlpatterns = [
	url(r'^$', views.index, name="index"),	
	url(r'^test/$', views.test, name="test"),	
	url(r'^maduracion/$', views.reporte_maduracion, name="reporte_maduracion"),	
	url(r'^algas/$', views.reporte_algas, name="reporte_algas"),

	url(r'^rpt1/$', views.rpt1, name="rpt1"),	
	url(r'^rpt2/$', views.rpt2, name="rpt2"),	
	url(r'^rpt3/$', views.rpt3, name="rpt3"),	
]
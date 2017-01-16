from django.conf.urls import url
from . import views

# /reporte/

urlpatterns = [
	url(r'^$', views.index, name="index"),	
	url(r'^test/$', views.test, name="test"),	
	url(r'^maduracion/$', views.reporte_maduracion, name="reporte_maduracion"),	
	url(r'^algas/$', views.reporte_algas, name="reporte_algas"),	
]
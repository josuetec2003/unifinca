from django.conf.urls import url
from . import views

# /larvarios/

urlpatterns = [
	url(r'^$', views.index, name="index"),	
	url(r'^nuevo-ciclo/$', views.nuevo_ciclo, name="nuevo_ciclo"),	
	url(r'^cerrar-ciclo/$', views.cerrar_ciclo, name="cerrar_ciclo"),	
	url(r'^verificar-ciclo-activo/$', views.verificar_ciclo_activo, name="verificar_ciclo_activo"),	
	url(r'^parametros-agua/(?P<id>\d+)/$', views.parametros_agua, name="parametros_agua"),
	url(r'^parametros-agua/guardar/$', views.parametros_agua_guardar, name="parametros_agua_guardar"),
]
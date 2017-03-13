from django.conf.urls import url
from . import views

# /larvarios/

urlpatterns = [
	url(r'^$', views.index, name="index"),	
	url(r'^nuevo-ciclo/$', views.nuevo_ciclo, name="nuevo_ciclo"),	
	url(r'^cerrar-ciclo/$', views.cerrar_ciclo, name="cerrar_ciclo"),	
	url(r'^verificar-ciclo-activo/$', views.verificar_ciclo_activo, name="verificar_ciclo_activo"),	
	url(r'^parametros-agua/(?P<id>\d+)/$', views.parametros_agua, name="parametros_agua"),
	url(r'^datos-larva/(?P<id>\d+)/$', views.datos_larva, name="datos_larva"),
	url(r'^parametros-agua/guardar/$', views.parametros_agua_guardar, name="parametros_agua_guardar"),
	url(r'^datos-larva/guardar/$', views.datos_larva_guardar, name="datos_larva_guardar"),
	url(r'^filtrar-params-agua/$', views.filtrar_params_agua, name="filtrar_params_agua"),
]
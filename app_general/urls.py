from django.conf.urls import url
from . import views

# /general/

urlpatterns = [
	url(r'^guardar-microbiologia/$', views.guardar_microbiologia, name="guardar_microbiologia"),	
	url(r'^parametros-agua/guardar/$', views.guardar_params_agua, name="guardar_params_agua"),	
	url(r'^filtrar-microbiologia/$', views.filtrar_microbiologia, name="filtrar_microbiologia"),
	url(r'^filtrar-params-agua/$', views.filtrar_params_agua, name="filtrar_params_agua"),
]
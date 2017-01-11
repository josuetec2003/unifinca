from django.conf.urls import url
from . import views

# /general/

urlpatterns = [
	url(r'^guardar-microbiologia/$', views.guardar_microbiologia, name="guardar_microbiologia"),	
	url(r'^filtrar-microbiologia/$', views.filtrar_microbiologia, name="filtrar_microbiologia"),	
]
from django.conf.urls import url
from . import views

# /maduracion/

urlpatterns = [
	url(r'^$', views.index, name="index"),	
	url(r'^guardar-datos-maduracion/$', views.guardar_datos_maduracion, name="guardar_datos_maduracion"),	
]
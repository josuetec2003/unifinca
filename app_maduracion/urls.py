from django.conf.urls import url
from . import views

# /maduracion/

urlpatterns = [
	url(r'^$', views.index, name="index"),	
	url(r'^sala/(?P<id>\d+)/$', views.datos_maduracion, name="datos_maduracion"),
	url(r'^guardar-datos/$', views.guardar_datos, name="guardar_datos"),
]
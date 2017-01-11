from django.conf.urls import url
from . import views

# /algas/

urlpatterns = [
	url(r'^$', views.index, name="index"),	
	url(r'^guardar-conteo/$', views.guardar_conteo, name="guardar_conteo"),	
]
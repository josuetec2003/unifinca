"""unifinca URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from app_general import views

urlpatterns = [    
    url(r'^$', views.form_login, name='form_login'),
    url(r'^login/$', views.validate_login, name='validate_login'),
    url(r'^logout/$', views.sign_off, name='sign_off'),
    url(r'^admin/', admin.site.urls),
    url(r'^algas/', include('app_algas.urls')),
    url(r'^dashboard/', include('app_dashboard.urls')),
    url(r'^general/', include('app_general.urls')),
    url(r'^larvarios/', include('app_larvarios.urls')),
    url(r'^maduracion/', include('app_maduracion.urls')),
    url(r'^reporte/', include('app_reportes.urls')),
]

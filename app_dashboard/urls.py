from django.conf.urls import url
from . import views

# /dashboard/

urlpatterns = [
	url(r'^$', views.dashboard, name="dashboard")
]
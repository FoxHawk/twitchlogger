from django.urls import path

from . import views

urlpatterns = [
	path('subbedevents', views.fetchSubbedEvents),
	path('loadlogs', views.fetchLogs),
	path("getchannels", views.getLoggedChannels),
	path('makereport', views.makeReport),
]
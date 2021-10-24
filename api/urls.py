from django.urls import path

from . import views

urlpatterns = [
	path('subbedevents', views.fetchSubbedEvents),
]
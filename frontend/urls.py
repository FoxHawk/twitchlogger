from django.urls import path

from . import views

urlpatterns = [
	path("", views.index),
	path("manage", views.manage),
	path("manage/removeChannel", views.manageDelete),
	path("manage/toggleEvent", views.manageToggleEvent),
	path("manage/addChannel", views.manageAdd),
	path("report", views.report),
]
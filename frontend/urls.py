from django.urls import path

from .Views import Index, Manage, Reports

urlpatterns = [
	path("", Index.index),
	path("manage", Manage.index),
	path("manage/removeChannel", Manage.delete),
	path("manage/toggleEvent", Manage.toggleEvent),
	path("manage/addChannel", Manage.add),
	path("report", Reports.index),
]
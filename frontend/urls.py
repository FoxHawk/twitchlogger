from django.urls import path


from .Views import Index, Manage, Reports, Channel

urlpatterns = [
	path("", Index.index),
	path("manage", Manage.index),
	path("manage/removeChannel", Manage.delete),
	path("manage/toggleEvent", Manage.toggleEvent),
	path("manage/addChannel", Manage.add),
	path("channel/<str:channel>", Channel.index),
	path("report", Reports.index),
]
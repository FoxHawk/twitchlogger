from django.http import HttpRequest, HttpResponse
from django.template import loader

from frontend.Views import templateFactory

def index(request: HttpRequest):
	if(request.method == "POST"):
		print(request.POST)

	template = templateFactory.buildTemplate("report.html", {}, request)
	return HttpResponse(template)
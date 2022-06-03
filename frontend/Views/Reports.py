from django.http import HttpRequest, HttpResponse
from django.template import loader

def index(request: HttpRequest):
	if(request.method == "POST"):
		print(request.POST)
	#load and render the template, then send a response with the rendered template
	template = loader.get_template("report.html")
	context = {}
	return HttpResponse(template.render(context=context, request=request))
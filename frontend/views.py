from django.http.response import HttpResponseBadRequest, HttpResponseServerError
from django.http import HttpRequest, HttpResponse
from django.template import loader
from api import manageSubscriptions

# Create your views here.

def index(request: HttpRequest):
	tp = loader.get_template("index.html")
	return HttpResponse(tp.render(request=request))

def manage(request: HttpRequest):
	if (request.method == "POST"):
		if("action" not in request.POST or "channel" not in request.POST): #if the post data doesn't include "action" or "channel", return bad request error
			return HttpResponseBadRequest()
		if(request.POST["action"] == "add"): #if the user wants to subscribe to a channel
			return manageAdd(request)
		elif(request.POST["action"] == "delete"): #if the user wants to unsubscribe from a channel
			return manageDelete(request)
		else:
			return HttpResponseBadRequest()#TODO: Create Error template pages

	if (request.method == "GET"):
		return manageGet(request)

def manageDelete(request: HttpRequest):
	if (not manageSubscriptions.unsubscribeFromChannel(request.POST["channel"])):
		return HttpResponseServerError()#TODO: Create Error template pages
	else:
		return manageGet(request)

def manageAdd(request: HttpRequest):
	if (not manageSubscriptions.subscribeToChannel(request.POST["channel"])):
		return HttpResponseServerError()#TODO: Create Error template pages
	else:
		return manageGet(request)

def manageGet(request: HttpRequest):
	template = loader.get_template("manage.html")
	context = {}
	return HttpResponse(template.render(context=context, request=request))

def report(request: HttpRequest):
	if(request.method == "POST"):
		print(request.POST)

	template = loader.get_template("report.html")
	context = {}
	return HttpResponse(template.render(context=context, request=request))
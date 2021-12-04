from django.http.response import HttpResponseBadRequest, HttpResponseServerError
from django.http import HttpRequest, HttpResponse
from django.template import loader
import requests
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
	#attempt to unsubscribe from the twitch eventsub event
	#if unsuccessful, return a 500 Server Error response
	if not manageSubscriptions.unsubscribeFromLiveEvent(request.POST["channel"]):
		return HttpResponseServerError()#TODO: Create Error template pages
	elif not manageSubscriptions.unsubscribeFromUpdateEvent(requests.POST["channel"]):
		return HttpResponseServerError()#TODO: Create Error template pages
	else:
		return manageGet(request) #respond with the management page

def manageAdd(request: HttpRequest):
	#attempt to subscribe to the twitch eventsub event for when a channel goes live
	#if unsuccessful, return a 500 Server Error response
	if not manageSubscriptions.subscribeToLiveEvent(request.POST["channel"]):
		return HttpResponseServerError()#TODO: Create Error template pages
	elif not manageSubscriptions.subscribeToUpdateEvent(request.POST["channel"]):
		return HttpResponseServerError()#TODO: Create Error template pages
	else:
		return manageGet(request) #respond with the management page

def manageGet(request: HttpRequest):
	template = loader.get_template("manage.html") #load the management page template
	context = {}
	return HttpResponse(template.render(context=context, request=request)) #return the rendered template page

def report(request: HttpRequest):
	if(request.method == "POST"):
		print(request.POST)
	#load and render the template, then send a response with the rendered template
	template = loader.get_template("report.html")
	context = {}
	return HttpResponse(template.render(context=context, request=request))
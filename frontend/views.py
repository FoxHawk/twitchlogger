from django.http.response import HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import loader
from django.utils.safestring import mark_safe
import requests
from twitchEvents.models import LogEntry
from . import manageSubscriptions

# Create your views here.

def index(request: HttpRequest):
	tp = loader.get_template("index.html")

	context = {"a":"b"}

	return HttpResponse(tp.render(context=context, request=request))

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
	data = manageSubscriptions.getSubscribedEvents()

	template = loader.get_template("manage.html")
	row = loader.get_template("manage/tableTemplate.html")

	rows = []

	for i in data:
		r = {}
		r["channel"] = manageSubscriptions.getUserData(i[1])["display_name"]
		r["id"] = i[0]
		rows.append(row.render(context=r, request=request))

	if (len(rows) == 0):
		return render(request, "manage.html")
	
	context = {}
	context["tableBody"] = rows
	return HttpResponse(template.render(context=context, request=request))
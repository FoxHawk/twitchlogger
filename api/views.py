from django.http.response import HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import loader
import json
import manageSubscriptions

# Create your views here.

def fetchSubbedEvents(request: HttpRequest):
	events = manageSubscriptions.getSubscribedEvents()

	return HttpResponse(json.dumps(events))

def fetchLogs(request: HttpRequest):
	pass
from django.http.response import HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import loader
import json
from . import manageSubscriptions

# Create your views here.

def fetchSubbedEvents(request: HttpRequest):
	data = manageSubscriptions.getSubscribedEvents()
	
	rows = []

	for i in data:
		r = {}
		r["channel"] = manageSubscriptions.getUserData(i[1])["display_name"]
		r["id"] = i[0]
		rows.append(r)

	return HttpResponse(json.dumps(rows))

def fetchLogs(request: HttpRequest):
	pass
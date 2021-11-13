from django.http.response import HttpResponseBadRequest, HttpResponseServerError
from django.http import HttpRequest, HttpResponse
import json
from django.core import serializers
from . import manageSubscriptions
from twitchEvents.models import LogEntry

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
	logs = LogEntry.objects.all().order_by("-startedAt")
	data = serializers.serialize("json", logs)

	return HttpResponse(data)


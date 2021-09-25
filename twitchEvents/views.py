from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json

from .models import LogEntry

# Create your views here.
@csrf_exempt
def endpoint(request: HttpRequest):
	data = json.loads(request.body)
	print(data)

	if("challenge" in data):
		return HttpResponse(data["challenge"])
	
	if("subscription" not in data or "status" not in data["subscription"] or data["subscription"]["status"] != "enabled"):
		return HttpResponseBadRequest()

	event = data["event"]

	le = LogEntry(channel=event["broadcaster_user_id"], startedAt=event["started_at"], eventID=event["id"], type=event["type"])
	le.save()
	return HttpResponse()
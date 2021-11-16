from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json

from api import manageSubscriptions
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

	chanData = manageSubscriptions.getChannelData(event["broadcaster_user_id"])

	le = LogEntry(channel=event["broadcaster_user_name"], startedAt=event["started_at"], eventID=event["id"], game=chanData["game_name"], title=chanData["title"])
	le.save()
	return HttpResponse()
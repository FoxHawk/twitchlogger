from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json

from api import manageSubscriptions
from .models import LogEntry

@csrf_exempt
def endpoint(request: HttpRequest):
	data = json.loads(request.body) #convert JSON post data to python object
	print(data)

	#if the request is a twitch api challenge request, respond with the text in the "challenge" variable under "data" in the request JSON
	if("challenge" in data):
		return HttpResponse(data["challenge"])
	#Catch any requests that do not contain the fields that we expect to be there
	if("subscription" not in data or "status" not in data["subscription"] or data["subscription"]["status"] != "enabled"):
		return HttpResponseBadRequest()

	event = data["event"] #all data under "event" variable

	chanData = manageSubscriptions.getChannelData(event["broadcaster_user_id"]) #get the channel data from the channel's user id

	#create and save a new log entry
	le = LogEntry(channel=event["broadcaster_user_name"], startedAt=event["started_at"], eventID=event["id"], game=chanData["game_name"], title=chanData["title"])
	le.save()
	return HttpResponse() #return a 200 OK response
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
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

	le = LogEntry(channel=event["broadcaster_user_name"], type=data["subscription"]["type"])

	if data["subscription"]["type"] == "channel.update": #if this is a channel update event
		le.datetimestamp=timezone.now()
		le.game = event["category_name"]
		le.title = event["title"]
	elif data["subscription"]["type"] == "stream.online": #if this is a stream live event
		chanData = manageSubscriptions.getChannelData(event["broadcaster_user_id"]) #get the stream info from the channel's user id

		le.datetimestamp = event["started_at"] #the event holds when the stream went live
		#get the game name and stream title from the channel data
		le.game = chanData["game_name"]
		le.title = chanData["title"]
	elif data["subscription"]["type"] == "stream.offline": #if this is a stream offline event
		#the stream offline event only contains the channel name
		le.datetimestamp = timezone.now()
		#we cannot get the stream data as the stream is offline
		le.game = "N/A"
		le.title = "N/A"
	
	le.save()

	return HttpResponse() #return a 200 OK response
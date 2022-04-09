from datetime import datetime
from typing import Dict
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json

from api import manageSubscriptions
from .models import LogEntry

@csrf_exempt
def endpoint(request: HttpRequest):
	try:
		data = json.loads(request.body) #convert JSON post data to python object
		print(data) #TODO: remove
	except json.decoder.JSONDecodeError:
		#if the json library can't decode the body into valid json, return a 400 bad request response
		return HttpResponseBadRequest()

	#if the request is a twitch api challenge request, respond with the text in the "challenge" variable under "data" in the request JSON
	if isChallengeRequest(data):
		return HttpResponse(data["challenge"])
	#Catch any requests that do not contain the fields that we expect to be there
	if isBadRequest(data, request.headers):
		return HttpResponseBadRequest()
	#Ignore any duplicate events
	if(isDuplicateEvent(request)):
		#Acknowledge the event
		return HttpResponse()

	log = getLogEntry(data, request.headers) #get LogEntry object with channel data pre-populated

	if data["subscription"]["type"] == "channel.update": #if this is a channel update event
		log = handleStreamUpdateEvent(log, data)
	elif data["subscription"]["type"] == "stream.online": #if this is a stream live event
		log = handleStreamLiveEvent(log, data)
	elif data["subscription"]["type"] == "stream.offline": #if this is a stream offline event
		log = handleStreamOfflineEvent(log, data)
	
	log.save() #record the LogEntry object to the database

	return HttpResponse() #return a 200 OK response

def isChallengeRequest(requestBody: Dict) -> bool:
	return "challenge" in requestBody

def isBadRequest(requestBody: Dict, headers: Dict) -> bool:
	"""Checks whether the twitch api request contains the correct json path

	Args:
		requestBody (Dict): The body of the request parsed as json
		request (HttpRequest): The Http Request object from the twitch api request

	Returns:
		boolean: Whether the request is incorrect or not (True on bad request)
	"""
	if "subscription" not in requestBody:
		return True
	
	if "status" not in requestBody["subscription"]:
		return True

	if requestBody["subscription"]["status"] != "enabled":
		return True

	if "Twitch-Eventsub-Message-Id" not in headers:
		print("Missing headers", headers.values())
		return True
	
	return False

def isDuplicateEvent(request: HttpRequest) -> bool:
	"""Checks if the event id has been recorded already

	Args:
		request (HttpRequest): The request object from the twitch api request

	Returns:
		bool: If the event is a duplicate
	"""
	eventID = request.headers["Twitch-Eventsub-Message-Id"]

	logs = LogEntry.objects.filter(eventid=eventID)

	return logs.count() != 0

def getLogEntry(requestBody: Dict, headers: Dict) -> LogEntry:
	"""Instantiates a new LogEvent object from the twitch api request

	Args:
		requestBody (Dict): The parsed body of the request
		request (HttpRequest): The request object from the twitch api request

	Returns:
		LogEntry: The Instantiated LogEntry object
	"""
	type = requestBody["subscription"]["type"]
	eventId = headers["Twitch-Eventsub-Message-Id"]

	log = LogEntry(type=type, eventid=eventId)

	return log

def handleStreamUpdateEvent(log: LogEntry, requestBody: Dict) -> LogEntry:
	"""Inputs data from a "channel.update" event into a LogEntry

	Args:
		log (LogEntry): The instantiated LogEntry to input the event data to
		requestBody (Dict): The parsed body from the twitch api request

	Returns:
		LogEntry: The LogEntry object with added event data
	"""
	eventData = requestBody["event"]
	
	log.datetimestamp = datetime.now()
	log.game = eventData["category_name"]
	log.title = eventData["title"]
	log.channel = eventData["broadcaster_user_name"]

	return log

def handleStreamLiveEvent(log: LogEntry, requestBody: Dict) -> LogEntry:
	"""Inputs data from a "stream.online" event into a LogEntry

	Args:
		log (LogEntry): The instantiated LogEntry to input the event data in to
		requestBody (Dict): The parsed twitch api request body

	Returns:
		LogEntry: The LogEntry object with added event data
	"""
	#fetch stream data from twith api endpoint as it is not included in event data
	channelData = manageSubscriptions.getChannelData(requestBody["event"]["broadcaster_user_id"])

	log.datetimestamp = requestBody["event"]["started_at"]#the event holds when the stream went live
	#get the game name and stream title from the channel data
	log.game = channelData["game_name"]
	log.title = channelData["title"]
	log.channel = requestBody["event"]["broadcaster_user_name"]

	return log

def handleStreamOfflineEvent(log: LogEntry, requestBody: Dict) -> LogEntry:
	"""Inputs data from a "stream.offline" event into a LogEntry

	Args:
		log (LogEntry): The instantiated LogEntry object
		requestBody (Dict): The parsed twitch api request body

	Returns:
		LogEntry: The LogEntry object with added data
	"""

	log.datetimestamp = requestBody["subscription"]["created_at"]
	#we cannot get the game or title if there isn't a live stream so use default values
	log.game = "N/A"
	log.title = "N/A"
	log.channel = requestBody["event"]["broadcaster_user_name"]

	return log

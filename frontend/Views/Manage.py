from django.shortcuts import redirect
from django.utils import timezone
from django.http.response import HttpResponseBadRequest, HttpResponseServerError
from django.http import HttpRequest, HttpResponse
from django.template import loader
from api import manageSubscriptions
from frontend.Views import templateFactory
from twitchEvents.models import LogEntry, ChannelEvents

def index(request: HttpRequest):
	data = ChannelEvents.objects.all().extra(select={"lower_channel": "lower(\"channelName\")"}).order_by("lower_channel")
	events = []

	for i in data:
		events.append({"channel": i.channelName, "streamUp": i.streamUp, "streamDown": i.streamDown, "streamUpdate": i.streamUpdate})

	template = templateFactory.buildTemplate("manage.html", {"events": events}, request)
	return HttpResponse(template)

def toggleEvent(request: HttpRequest):
	if "channel" not in request.GET or "event" not in request.GET:
		return HttpResponseBadRequest("Error: Missing paramaters")

	channel = request.GET["channel"]
	event = request.GET["event"]

	if event not in ("channel.update", "stream.online", "stream.offline"):
		return HttpResponseBadRequest("Error: Incorrect event type. Event: " + event)

	mChannel = ChannelEvents.objects.filter(channelName=channel)

	if len(mChannel) <= 0:
		return HttpResponseBadRequest("Error: Channel not subscribed to")
	mChannel = mChannel[0]

	state = mChannel.getState(event)
	print(channel, event, state)

	if not state:
		print("Subscribing to", channel, event)
		if not manageSubscriptions.subscribeToEvent(channel, event):
			return HttpResponseServerError()
	else:
		print("Unsubscribing from", channel, event)
		if not manageSubscriptions.unsubscribeFromEvent(channel, event):
			return HttpResponseServerError()

	mChannel.setState(event, not state)
	return redirect("/manage")

def delete(request: HttpRequest):
	if "channel" not in request.GET:
		return HttpResponseBadRequest()

	channelName = request.GET["channel"]
	#attempt to unsubscribe from the twitch eventsub events
	#if unsuccessful, return a 500 Server Error response
	if not manageSubscriptions.unsubscribeFromAllEvents(channelName):
		return HttpResponseServerError()#TODO: Create Error template pages
	else:
		#delete the database entry
		ChannelEvents.objects.filter(channelName=channelName).delete()
		return redirect("/manage") #respond with the management page

def add(request: HttpRequest):
	if "channel" not in request.POST:
		return HttpResponseBadRequest()

	channelName = request.POST["channel"]
	#attempt to subscribe to the twitch eventsub events
	#if unsuccessful, return a 500 Server Error response
	if not manageSubscriptions.subscribeToAllEvents(channelName):
		return HttpResponseServerError()#TODO: Create Error template pages
	else:
		channelID = manageSubscriptions.getUserID(channelName)
		#create a new database entry for the channel
		ChannelEvents.objects.create(channelID=channelID, channelName=channelName).save()

		return redirect("/manage") #respond with the management page
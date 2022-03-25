from django.shortcuts import redirect
from django.utils import timezone
from django.http.response import HttpResponseBadRequest, HttpResponseServerError
from django.http import HttpRequest, HttpResponse
from django.template import loader
from api import manageSubscriptions
from twitchEvents.models import LogEntry, ChannelEvents

# Create your views here.

def index(request: HttpRequest):
	channels = None
	#if the from date or to date were supplied, use the default values of the beginning of the day to now
	if "fromDate" not in request.GET.keys() or "toDate" not in request.GET.keys():
		channels = getStreamers(timezone.now().replace(hour=0, minute=0, second=0, microsecond=0), timezone.now())
	else:
		channels = getStreamers(request.GET["fromDate"], request.GET["toDate"])

	#load the template and render it with the channels in the context
	tp = loader.get_template("index.html")
	return HttpResponse(tp.render(request=request, context={"streamers": channels}))

def getStreamers(dateFrom: timezone, dateTo: timezone):
	data = LogEntry.objects.filter(datetimestamp__gte=dateFrom, datetimestamp__lte=dateTo).exclude(game="N/A").exclude(game="")
	channels = []

	#create a list entry for every unique channel
	for i in data.values("channel").distinct().extra(select={"lower_channel": "lower(channel)"}).order_by("lower_channel"):
		channels.append({"name": i["channel"], "games": []})
	
	for i in channels: #fill out the games that were played between the datetime durations
		for j in data.filter(channel=i["name"]).order_by("-datetimestamp").values("datetimestamp", "game", "title"):
			i["games"].append({"timestamp": j["datetimestamp"], "game": j["game"], "title": j["title"]})
	
	return channels

def manage(request: HttpRequest):
	data = ChannelEvents.objects.all().extra(select={"lower_channel": "lower(\"channelName\")"}).order_by("lower_channel")
	events = []

	for i in data:
		events.append({"channel": i.channelName, "streamUp": i.streamUp, "streamDown": i.streamDown, "streamUpdate": i.streamUpdate})

	template = loader.get_template("manage.html") #load the management page template
	context = {"events": events}
	return HttpResponse(template.render(context=context, request=request)) #return the rendered template page

def manageToggleEvent(request: HttpRequest):
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

def manageDelete(request: HttpRequest):
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

def manageAdd(request: HttpRequest):
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

def report(request: HttpRequest):
	if(request.method == "POST"):
		print(request.POST)
	#load and render the template, then send a response with the rendered template
	template = loader.get_template("report.html")
	context = {}
	return HttpResponse(template.render(context=context, request=request))
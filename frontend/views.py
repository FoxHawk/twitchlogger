from datetime import timedelta
from django.utils import timezone
from django.http.response import HttpResponseBadRequest, HttpResponseServerError
from django.http import HttpRequest, HttpResponse
from django.template import loader
from api import manageSubscriptions
from twitchEvents.models import LogEntry

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
	for i in data.values("channel").distinct():
		channels.append({"name": i["channel"], "games": []})
	
	for i in channels: #fill out the games that were played between the datetime durations
		for j in data.filter(channel=i["name"]).values("datetimestamp", "game"):
			i["games"].append({"timestamp": j["datetimestamp"], "game": j["game"]})
	
	return channels

def manage(request: HttpRequest):
	if (request.method == "POST"):
		if("action" not in request.POST or "channel" not in request.POST): #if the post data doesn't include "action" or "channel", return bad request error
			return HttpResponseBadRequest()
		if(request.POST["action"] == "add"): #if the user wants to subscribe to a channel
			return manageAdd(request)
		elif(request.POST["action"] == "delete"): #if the user wants to unsubscribe from a channel
			return manageDelete(request)
		else:
			return HttpResponseBadRequest()#TODO: Create Error template pages

	if (request.method == "GET"):
		return manageGet(request)

def manageDelete(request: HttpRequest):
	#attempt to unsubscribe from the twitch eventsub events
	#if unsuccessful, return a 500 Server Error response
	if not manageSubscriptions.unsubscribeFromAllEvents(request.POST["channel"]):
		return HttpResponseServerError()#TODO: Create Error template pages
	else:
		return manageGet(request) #respond with the management page

def manageAdd(request: HttpRequest):
	#attempt to subscribe to the twitch eventsub events
	#if unsuccessful, return a 500 Server Error response
	if not manageSubscriptions.subscribeToAllEvents(request.POST["channel"]):
		return HttpResponseServerError()#TODO: Create Error template pages
	else:
		return manageGet(request) #respond with the management page

def manageGet(request: HttpRequest):
	template = loader.get_template("manage.html") #load the management page template
	context = {}
	return HttpResponse(template.render(context=context, request=request)) #return the rendered template page

def report(request: HttpRequest):
	if(request.method == "POST"):
		print(request.POST)
	#load and render the template, then send a response with the rendered template
	template = loader.get_template("report.html")
	context = {}
	return HttpResponse(template.render(context=context, request=request))
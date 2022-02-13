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
	if "fromDate" not in request.GET.keys() or "toDate" not in request.GET.keys():
		channels = getStreamers(timezone.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=7), timezone.now())
	else:
		channels = getStreamers(request.GET["fromDate"], request.GET["toDate"])


	tp = loader.get_template("index.html")
	return HttpResponse(tp.render(request=request, context={"streamers": channels}))

def getStreamers(dateFrom: timezone, dateTo: timezone):
	data = LogEntry.objects.filter(datetimestamp__gte=dateFrom, datetimestamp__lte=dateTo)
	channels = []

	for i in data.values("channel").distinct():
		channels.append({"name": i["channel"], "games": []})
	
	for i in channels:
		for j in data.filter(channel=i["name"]).values("datetimestamp", "game"):
			if j["game"] == "N/A" or j["game"] == "":
				continue
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
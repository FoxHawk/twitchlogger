from datetime import datetime
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect, HttpResponseServerError
from django.http import HttpRequest, HttpResponse
import json
from django.core import serializers
from . import manageSubscriptions
from twitchEvents.models import LogEntry
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.utils import timezone

# Create your views here.

def fetchSubbedEvents(request: HttpRequest):
	data = manageSubscriptions.getSubscribedEvents() #get a list of events that we are subscribed to
	
	rows = []
	#package the data into an array of dicts
	for i in data:
		r = {}
		r["channel"] = manageSubscriptions.getUserData(i["condition"]["broadcaster_user_id"])["display_name"]
		r["status"] = i["status"]
		r["type"] = i["type"]
		rows.append(r)

	return HttpResponse(json.dumps(rows)) #respond with a json string of the data

def fetchLogs(request: HttpRequest):
	data = ""
	fromDate, toDate = None, None

	#if the request is a post request, check for a "fromDate" and "toDate" POST variable
	if request.method == "POST" and "fromDate" in request.POST and "toDate" in request.POST:
		#use fromDate and toDate from user
		fromDate = request.POST["fromDate"]
		toDate = request.POST["toDate"]
	else: #
		#get logs between the beginning of today and the end of today
		fromDate = timezone.now().replace(hour=0, minute=0, second=0)
		toDate = timezone.now().replace(hour=23, minute=59, second=59)
	
	#get logs between the fromDate and toDate (inclusive)
	logs = LogEntry.objects.filter(datetimestamp__gte=fromDate, datetimestamp__lte=toDate).order_by("-datetimestamp")
	#Use django's json serialiser to convert the logs object to a json string
	data = serializers.serialize("json", logs)
	return HttpResponse(data)

def getLoggedChannels(request: HttpRequest):
	#get every channel name that appears in the logs (distinct selects each value only once)
	logs = LogEntry.objects.values("channel").distinct()

	channels = []
	#load the values into an array (simplified from a django model list object)
	for i in logs:
		channels.append(i["channel"])
	
	return HttpResponse(json.dumps(channels)) #return the channels as a json array

def makeReport(request: HttpRequest):
	#get the from & to variables from the POST dict
	dateFrom = request.POST["From"]
	dateTo = request.POST["To"]

	channels = []
	#get all of the remaining keys and put them into an array (the keys are the channel names)
	for i in request.POST.keys():
		if i != "From" and i != "To" and i != "csrfmiddlewaretoken":
			channels.append(i)
	#select all logs which are from the channels in the array and are between the from and to datetimes
	logs = LogEntry.objects.filter(channel__in=channels, datetimestamp__gt=timezone.make_aware(datetime.fromisoformat(dateFrom)), datetimestamp__lt=timezone.make_aware(datetime.fromisoformat(dateTo)))

	data = []
	#add log data to an array in the form of dicts (an array of dicts)
	for i in logs:
		data.append({"channel": i.channel, "title": i.title, "game": i.game, "datetimestamp": i.datetimestamp, "type": i.type})

	context = {}

	#load the logs as well as the from and to datetimes
	context["data"] = data
	context["dateFrom"] = timezone.make_aware(datetime.fromisoformat(dateFrom))
	context["dateTo"] = timezone.make_aware(datetime.fromisoformat(dateTo))
	
	#render the email message
	html_message = render_to_string("api/mailReport.html", context=context)
	plain_message = strip_tags(html_message) #remove html for a text-only version
	#send the email
	send_mail("Twitch Streams Report", plain_message, "TwitchLog <twitchlogs@foxhawk.co.uk>", ["fox@foxhawk.co.uk"], html_message=html_message)

	return HttpResponseRedirect("/report") #Redirect back to the reports page
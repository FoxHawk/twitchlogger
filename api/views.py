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
		r["channel"] = manageSubscriptions.getUserData(i[1])["display_name"]
		r["status"] = i[0]
		rows.append(r)

	return HttpResponse(json.dumps(rows)) #respond with a json string of the data

def fetchLogs(request: HttpRequest):
	logs = LogEntry.objects.all().order_by("-startedAt") #Get all logs ordrred by startedAt descending (hence the "-" character)
	data = serializers.serialize("json", logs) #Use django's json serialiser to convert the logs object to a json string

	return HttpResponse(data)

def getLoggedChannels(request: HttpRequest):
	logs = LogEntry.objects.values("channel").distinct()

	channels = []

	for i in logs:
		channels.append(i["channel"])
	
	return HttpResponse(json.dumps(channels))

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
	logs = LogEntry.objects.filter(channel__in=channels, startedAt__gt=timezone.make_aware(datetime.fromisoformat(dateFrom)), startedAt__lt=timezone.make_aware(datetime.fromisoformat(dateTo)))

	data = []

	for i in logs:
		data.append({"channel": i.channel, "title": i.title, "game": i.game, "startedAt": i.startedAt})

	context = {}

	#load the logs and current date into the context
	context["data"] = data
	context["dateFrom"] = timezone.make_aware(datetime.fromisoformat(dateFrom))
	context["dateTo"] = timezone.make_aware(datetime.fromisoformat(dateTo))
	
	#render the email message
	html_message = render_to_string("api/mailReport.html", context=context)
	plain_message = strip_tags(html_message) #remove html for a text-only version
	#send the email
	send_mail("Twitch Streams Report", plain_message, "TwitchLog <twitchlogs@foxhawk.co.uk>", ["fox@foxhawk.co.uk"], html_message=html_message)

	return HttpResponseRedirect("/report") #Redirect back to the reports page
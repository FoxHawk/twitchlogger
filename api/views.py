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

def makeReport(request: HttpRequest):
	request.POST.pop("csrfmiddlewaretoken") #remove the CSRF token from the POST dict
	#get the from & to variables from the POST dict
	dateFrom = request.POST.pop("From")
	dateTo = request.POST.pop("To")

	channels = []
	#get all of the remaining keys and put them into an array (the keys are the channel names)
	for i in request.POST.keys():
		channels.append(i)
	#select all logs which are from the channels in the array and are between the from and to datetimes
	logs = LogEntry.objects.filter(channel=channels, startedAt__gt=dateFrom, startedAt__lt=dateTo)

	data = []

	for i in logs:
		data.append({"channel": i.channel, "title": i.title, "game": i.game, "startedAt": i.startedAt})
	
	context = {}

	#load the logs and current date into the context
	context["data"] = data
	context["dateFrom"] = timezone(dateFrom)
	context["dateTo"] = timezone(dateTo)
	
	#render the email message
	html_message = render_to_string("mail.html", context=context)
	plain_message = strip_tags(html_message) #remove html for a text-only version
	#send the email
	send_mail("Twitch Streams From Today", plain_message, "TwitchLog <twitchlogs@foxhawk.co.uk>", ["fox@foxhawk.co.uk"], html_message=html_message)

	return HttpResponseRedirect("/report") #Redirect back to the reports page
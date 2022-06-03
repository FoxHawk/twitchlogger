from time import time
from django.utils import timezone
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.template import loader
from twitchEvents.models import LogEntry
from . import templateFactory

def index(request: HttpRequest, channel: str):
	fromDate = None
	toDate = None

	#if there are no logs for this channel, return a 404 error
	if not channelExists(channel):
		return HttpResponseNotFound("<h1>Error: No logs for this channel were found</h1>")

	#if the from date or to date were supplied, use the default values of the beginning of the day to now
	if "fromDate" not in request.GET.keys() or "toDate" not in request.GET.keys():
		fromDate = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
		toDate = timezone.now()
	else:
		fromDate = request.GET["fromDate"]
		toDate = request.GET["toDate"]
	#get stream event logs between the dates for the specified channel
	channelData = getChannel(fromDate, toDate, channel)

	#load the template and render it with the channel logs in the context
	#tp = loader.get_template("channel.html")
	#return HttpResponse(tp.render(request=request, context={"streamer": channelData, "channel": channel}))
	template = templateFactory.buildTemplate("channel.html", {"streamer": channelData, "channel": channel}, request)
	return HttpResponse(template)

def getChannel(dateFrom: timezone, dateTo: timezone, channel: str):
	logs = []

	#get all logs between the start and end timestamps (inclusive) only for the specified channel
	data = LogEntry.objects.filter(datetimestamp__gte=dateFrom, datetimestamp__lte=dateTo, channel=channel)
	#remove any entries with N/A or missing game info (old data or stream offline events)
	data = data.exclude(game="N/A").exclude(game="")
	#order the data by the date-timestamp descending
	data = data.order_by("-datetimestamp")
	#only get the timestamp, game name, stream title, and event type
	data = data.values("datetimestamp", "game", "title", "type")

	return data


def channelExists(channel: str):
	#will be true if a log entry for this channel exists, false otherwise
	exists = LogEntry.objects.filter(channel=channel).exists()

	return exists
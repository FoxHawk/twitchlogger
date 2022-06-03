from django.utils import timezone
from django.http import HttpRequest, HttpResponse
from django.template import loader
from frontend.Views import templateFactory
from twitchEvents.models import LogEntry

def index(request: HttpRequest):
	channels = None
	#TODO: refactor (DRY)
	#if the from date or to date were supplied, use the default values of the beginning of the day to now
	if "fromDate" not in request.GET.keys() or "toDate" not in request.GET.keys():
		channels = getStreamers(timezone.now().replace(hour=0, minute=0, second=0, microsecond=0), timezone.now())
	else:
		channels = getStreamers(request.GET["fromDate"], request.GET["toDate"])

	template = templateFactory.buildTemplate("index.html", {"streamers": channels}, request)
	return HttpResponse(template)

def getStreamers(dateFrom: timezone, dateTo: timezone):
	data = LogEntry.objects.filter(datetimestamp__gte=dateFrom, datetimestamp__lte=dateTo).exclude(game="N/A").exclude(game="")
	channels = []

	#create a list entry for every unique channel
	for i in data.values("channel").distinct().extra(select={"lower_channel": "lower(channel)"}).order_by("lower_channel"):
		channels.append({"name": i["channel"], "games": []})
	
	for i in channels: #fill out the games that were played between the datetime durations
		for j in data.filter(channel=i["name"]).order_by("-datetimestamp").values("datetimestamp", "game", "title", "type"):
			i["games"].append({"timestamp": j["datetimestamp"], "game": j["game"], "title": j["title"], "type":j["type"]})
	
	return channels
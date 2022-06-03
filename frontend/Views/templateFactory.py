from django.db.models.functions import Lower
from django.template import loader
from twitchEvents.models import LogEntry
from django.http import HttpRequest

def buildTemplate(template: str, context: dict, request: HttpRequest):
	context["navbarChannels"] = getAllChannels()

	template = loader.get_template(template)
	renderedTemplate = template.render(request=request, context=context)

	return renderedTemplate

def getAllChannels():
	channels = LogEntry.objects.values_list("channel", flat=True).distinct("channel")
	#sort channels case-insensitive
	channels = sorted(channels, key=str.casefold)

	return channels
from django.core.management.base import BaseCommand
from api import manageSubscriptions
from twitchEvents.models import ChannelEvents

class Command(BaseCommand):

	def handle(self, *args, **options):
		channels = self.getSubbedEvents()
		self.updateDatabase(channels)
		self.cleanDatabase(channels)

	def getSubbedEvents(self):
		channels = {}
		subbedEvents = manageSubscriptions.getSubscribedEvents()

		for i in subbedEvents:
			channelID = i["condition"]["broadcaster_user_id"]

			if channelID not in channels:
				channel = manageSubscriptions.getChannelData(i["condition"]["broadcaster_user_id"])["broadcaster_name"]
				channels[channelID] = {"stream.online": False, "stream.offline": False, "channel.update": False,
				"channelName": channel}
			
			channels[channelID][i["type"]] = True
			print("Found", channelID, channels[channelID]["channelName"], i["type"])
		
		return channels

	def updateDatabase(self, channels):
		for i in channels:
			channel = channels[i]
			print("Updating", channel["channelName"], i)
			ChannelEvents.objects.update_or_create(channelID=i, channelName=channel["channelName"], streamUp=channel["stream.online"],
			streamDown=channel["stream.offline"],streamUpdate=channel["channel.update"])

	def cleanDatabase(self, channels):
		data = ChannelEvents.objects.all()
		for i in data:
			if i.channelID not in channels:
				print("Removing", i.channelID)
				ChannelEvents.objects.filter(channel=i.channelID).delete()

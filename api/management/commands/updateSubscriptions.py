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
			self.updateOrCreate(i, channel)
			# ChannelEvents.objects.update_or_create(channelID=i, channelName=channel["channelName"], streamUp=channel["stream.online"],
			# streamDown=channel["stream.offline"],streamUpdate=channel["channel.update"])

	def updateOrCreate(self, channelID, channel):
		events = ChannelEvents.objects.filter(channelID=channelID)
		if events.count() == 0:
			#create
			print("Creating", channel["channelName"])
			self.create(channelID, channel)
		else:
			#update
			print("Updating", channel["channelName"])
			self.update(events[0], channel)
	
	def update(self, eventObject: ChannelEvents, channel):
		eventObject.channelName = channel["channelName"]
		eventObject.streamUp = channel["stream.online"]
		eventObject.streamDown = channel["stream.offline"]
		eventObject.streamChanged = channel["channel.update"]

		eventObject.save()

	def create(self, channelID, channel):
		newEvent = ChannelEvents(channelID=channelID, channelName=channel["channelName"], streamUp=channel["stream.online"],
		streamDown=channel["stream.offline"], streamUpdate=channel["channel.update"])
		newEvent.save()

	def cleanDatabase(self, channels):
		#TODO: fixme
		data = ChannelEvents.objects.all()
		for i in data:
			if i.channelID not in channels:
				print("Removing", i.channelID)
				ChannelEvents.objects.filter(channelID=i.channelID).delete()

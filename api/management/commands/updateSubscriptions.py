from django.core.management.base import BaseCommand
from api import manageSubscriptions

class Command(BaseCommand):

	def handle(self, *args, **options):
		
		channels = []

		subbedEvents = manageSubscriptions.getSubscribedEvents()

		for i in subbedEvents:
			channel = manageSubscriptions.getChannelData(i["condition"]["broadcaster_user_id"])
			print(channel)
			channel = channel["broadcaster_name"]
			if channel not in channels:
				print("Found channel: " + channel)
				channels.append(channel)

		for i in channels:
			print("Updating channel: " + i)
			manageSubscriptions.subscribeToEvent(i, "stream.online")
			manageSubscriptions.subscribeToEvent(i, "stream.offline")
			manageSubscriptions.subscribeToEvent(i, "channel.update")
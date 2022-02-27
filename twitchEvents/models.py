from django.db import models

# Create your models here.

class LogEntry(models.Model):
	eventid = models.CharField(max_length=100)
	channel = models.CharField(max_length=50)
	datetimestamp = models.DateTimeField()
	game = models.CharField(max_length=100)
	title = models.CharField(max_length=200)
	type=models.CharField(max_length=20)

class ChannelEvents(models.Model):
	channelID = models.CharField(max_length=50, primary_key=True)
	channelName = models.CharField(max_length=50)
	streamUp = models.BooleanField(default=True)
	streamDown = models.BooleanField(default=True)
	streamUpdate = models.BooleanField(default=True)

	def getState(self, event: str):
		if event == "stream.online":
			return self.streamUp
		elif event == "channel.update":
			return self.streamChanged
		elif event == "stream.offline":
			return self.streamDown
		else:
			return False
	
	def setState(self, event: str, state: bool):
		if event == "stream.online":
			self.streamUp = state
		elif event == "channel.update":
			self.streamChanged = state
		elif event == "stream.offline":
			self.streamDown = state

		self.save()
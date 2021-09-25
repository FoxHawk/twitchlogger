from django.db import models

# Create your models here.

class LogEntry(models.Model):
	channelID = models.ForeignKey("EventEntry", on_delete=models.CASCADE)
	startedAt = models.DateTimeField()
	eventID = models.IntegerField()
	type = models.CharField(max_length=20)

class eventEntry(models.Model):
	id = models.CharField(max_length=30)
	channel = models.CharField(max_length=50, primary_key=True)
	channelID = models.CharField(max_length=20)
from django.db import models

# Create your models here.

class LogEntry(models.Model):
	channel = models.CharField(max_length=50)
	startedAt = models.DateTimeField()
	game = models.CharField(max_length=100)
	title = models.CharField(max_length=200)

class UpdateLogEntry(models.Model):
	channel = models.CharField(max_length=50)
	recieved = models.DateTimeField()
	game = models.CharField(max_length=100)
	title = models.CharField(max_length=200)
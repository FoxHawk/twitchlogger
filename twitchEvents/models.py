from django.db import models

# Create your models here.

class LogEntry(models.Model):
	channel = models.CharField(max_length=50)
	startedAt = models.DateTimeField()
	eventID = models.CharField(max_length=40)
	type = models.CharField(max_length=20)
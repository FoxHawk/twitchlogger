from django.db import models

# Create your models here.

class LogEntry(models.Model):
	channel = models.CharField(max_length=50)
	datetimestamp = models.DateTimeField()
	game = models.CharField(max_length=100)
	title = models.CharField(max_length=200)
	type=models.CharField(max_length=20)
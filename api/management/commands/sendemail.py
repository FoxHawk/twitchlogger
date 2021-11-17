from django.core.management.base import BaseCommand, CommandError
from twitchEvents.models import LogEntry
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class Command(BaseCommand):
	help = "Sends a notification email with all the streams that started at 8PM yesterday"

	def handle(self, *args, **options):
		#Get all logs starting at 8PM yesterday
		logs = LogEntry.objects.filter(startedAt__gte=timezone.now().replace(hour=20, minute=0, second=0) - timedelta(days=1))

		#if there are no logs, just exit
		if len(logs) == 0:
			return

		data = []
		context = {}

		#put logs into an array for the html template context
		for i in logs:
			data.append({"channel": i.channel, "title": i.title, "game": i.game, "startedAt": i.startedAt})
		
		#load the logs and current date into the context
		context["data"] = data
		context["date"] = timezone.now().date().isoformat()
		
		#render the email message
		html_message = render_to_string("mail.html", context=context)
		plain_message = strip_tags(html_message) #remove html for a text-only version
		#send the email
		send_mail("Twitch Streams From Today", plain_message, "TwitchLog <twitchlogs@foxhawk.co.uk>", ["fox@foxhawk.co.uk"], html_message=html_message)
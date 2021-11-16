from django.core.management.base import BaseCommand, CommandError
from twitchEvents.models import LogEntry
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class Command(BaseCommand):
	help = "Sends a notification email with all the streams that started today"

	def handle(self, *args, **options):
		logs = LogEntry.objects.filter(startedAt__gte=timezone.now().replace(hour=0, minute=0, second=0) - timedelta(days=2))

		if len(logs) == 0:
			return

		data = []
		context = {}

		for i in logs:
			data.append({"channel": i.channel, "title": i.title, "game": i.game, "startedAt": i.startedAt})
		
		context["data"] = data
		context["date"] = timezone.now().date().isoformat()
		
		html_message = render_to_string("mail.html", context=context)
		plain_message = strip_tags(html_message)
		#print(html_message)
		send_mail("Twitch Streams From Today", plain_message, "TwitchLog <twitchlog@foxhawk.co.uk>", ["fox@foxhawk.co.uk"], html_message=html_message)
		
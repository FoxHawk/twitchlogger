from urllib import response
from django.test import TestCase
from twitchEvents import views
from twitchEvents.models import LogEntry

# Create your tests here.

_post_path = "/logger/endpoint"
_twitch_header = "HTTP_Twitch-Eventsub-Message-Id"

class endpointChallengeTests(TestCase):
	def setUp(self):
		self.challenge = "pogchamp-kappa-360noscope-vohiyo"
		self.challengeJson = {"challenge": self.challenge, "subscription": { "id": "f1c2a387-161a-49f9-a165-0f21d7a4e1c4", "status": "webhook_callback_verification_pending", "type": "channel.follow", "version": "1", "cost": 1, "condition": {"broadcaster_user_id": "12826"}, "transport": {"method": "webhook", "callback": "https://example.com/webhooks/callback"}, "created_at": "2019-11-16T10:11:12.123Z"}}

	def test_challenge_request_post(self):
		response = self.client.post(_post_path, self.challengeJson, content_type="application/json")

		self.assertEqual(self.challenge, response.content.decode("utf-8"))

	def test_challenge_detection(self):
		challengeData = {"challenge": self.challenge}
		resp = views.isChallengeRequest(challengeData)

		self.assertTrue(resp)

	def test_not_challenge(self):
		data = {"a": "b"}
		resp = views.isChallengeRequest(data)

		self.assertFalse(resp)

"""
Tests for twitch event requests
"""
class endpointBadRequestTests(TestCase):
	def setUp(self):
		self.goodRequest = {"subscription":{"id":"f1c2a387-161a-49f9-a165-0f21d7a4e1c4","type":"stream.online","version":"1","status":"enabled","cost":0,"condition":{"broadcaster_user_id":"113954840"},"transport":{"method":"webhook","callback":"https://example.com/webhooks/callback"},"created_at":"2019-11-16T10:11:12.123Z"},"event":{"id":"9001","broadcaster_user_id":"12826","broadcaster_user_login":"cool_user","broadcaster_user_name":"Cool_User","type":"live","started_at":"2020-10-11T10:11:12.123Z"}}

	def test_bad_request_wrong_data_type_post(self):
		response = self.client.post(_post_path, "bad data", content_type="text/html", **{_twitch_header: "test"})
		self.assertEqual(response.status_code, 400)

	def test_bad_request_incorrect_json_post(self):
		response = self.client.post(_post_path, {"bad": "data"}, content_type="application/json")
		self.assertEqual(response.status_code, 400)

	def test_good_request_post(self):
		response = self.client.post(_post_path, self.goodRequest, content_type="application/json",  **{_twitch_header: "test"})
		self.assertEqual(response.status_code, 200)

class endpointEventTypeTests(TestCase):
	def test_stream_online_post(self):
		self.sendRequest({"subscription":{"id":"f1c2a387-161a-49f9-a165-0f21d7a4e1c4","type":"stream.online","version":"1","status":"enabled","cost":0,"condition":{"broadcaster_user_id":"113954840"},"transport":{"method":"webhook","callback":"https://example.com/webhooks/callback"},"created_at":"2019-11-16T10:11:12.123Z"},"event":{"id":"9001","broadcaster_user_id":"12826","broadcaster_user_login":"cool_user","broadcaster_user_name":"Cool_User","type":"live","started_at":"2020-10-11T10:11:12.123Z"}})

	def test_stream_offline_post(self):
		self.sendRequest({"subscription":{"id":"f1c2a387-161a-49f9-a165-0f21d7a4e1c4","type":"stream.offline","version":"1","status":"enabled","cost":0,"condition":{"broadcaster_user_id":"1337"},"created_at":"2019-11-16T10:11:12.123Z","transport":{"method":"webhook","callback":"https://example.com/webhooks/callback"}},"event":{"broadcaster_user_id":"12826","broadcaster_user_login":"cool_user","broadcaster_user_name":"Cool_User"}})

	def test_channel_updated_post(self):
		self.sendRequest({"subscription":{"id":"f1c2a387-161a-49f9-a165-0f21d7a4e1c4","type":"channel.update","version":"1","status":"enabled","cost":0,"condition":{"broadcaster_user_id":"1337"},"transport":{"method":"webhook","callback":"https://example.com/webhooks/callback"},"created_at":"2019-11-16T10:11:12.123Z"},"event":{"broadcaster_user_id":"12826","broadcaster_user_login":"cool_user","broadcaster_user_name":"Cool_User","title":"Best Stream Ever","language":"en","category_id":"21779","category_name":"Fortnite","is_mature":False}})

	def sendRequest(self, request):
		response = self.client.post(_post_path, request, content_type="application/json", **{_twitch_header: "test"})
		self.assertEqual(response.status_code, 200)

class endpointDuplicateRequestTests(TestCase):
	def setUp(self):
		self.sendRequest()

	def test_duplicate_event_post(self):
		response = self.sendRequest()
		self.assertEqual(response.status_code, 200)

	def sendRequest(self):
		response = self.client.post(_post_path, {"subscription":{"id":"f1c2a387-161a-49f9-a165-0f21d7a4e1c4","type":"stream.online","version":"1","status":"enabled","cost":0,"condition":{"broadcaster_user_id":"113954840"},"transport":{"method":"webhook","callback":"https://example.com/webhooks/callback"},"created_at":"2019-11-16T10:11:12.123Z"},"event":{"id":"9001","broadcaster_user_id":"12826","broadcaster_user_login":"cool_user","broadcaster_user_name":"Cool_User","type":"live","started_at":"2020-10-11T10:11:12.123Z"}}, content_type="application/json", **{_twitch_header: "test"})
		return response

class endpointGetLogEntryTests(TestCase):
	def setUp(self):
		pass

	def test_get_LogEntry(self):
		pass



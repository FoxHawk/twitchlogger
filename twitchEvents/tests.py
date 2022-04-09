from django.test import TestCase
from twitchEvents import views

# Create your tests here.

class endpointChallengeTests(TestCase):
	def setUp(self):
		self.challenge = "pogchamp-kappa-360noscope-vohiyo"
		self.challengeJson = {"challenge": self.challenge, "subscription": { "id": "f1c2a387-161a-49f9-a165-0f21d7a4e1c4", "status": "webhook_callback_verification_pending", "type": "channel.follow", "version": "1", "cost": 1, "condition": {"broadcaster_user_id": "12826"}, "transport": {"method": "webhook", "callback": "https://example.com/webhooks/callback"}, "created_at": "2019-11-16T10:11:12.123Z"}}

	def test_challenge_request_post(self):
		response = self.client.post("/logger/endpoint", self.challengeJson, content_type="application/json")

		self.assertEqual(self.challenge, response.content.decode("utf-8"))

	def test_challenge_detection(self):
		challengeData = {"challenge": self.challenge}
		resp = views.isChallengeRequest(challengeData)

		self.assertTrue(resp)

	def test_not_challenge(self):
		data = {"a": "b"}
		resp = views.isChallengeRequest(data)

		self.assertFalse(resp)

class endpointBadRequestTests(TestCase):
	def setUp(self):
		pass

	def test_bad_request_post(self):
		pass

	def test_good_request_post(self):
		pass

	def test_bad_request(self):
		pass

	def test_good_request(self):
		pass

class endpointDuplicateRequestTests(TestCase):
	def setUp(self):
		pass

	def test_duplicate_event_post(self):
		pass

	def test_non_duplicate_event_post(self):
		pass

	def test_duplicate_event(self):
		pass

	def test_non_duplicate_event(self):
		pass

class endpointGetLogEntryTests(TestCase):
	def setUp(self):
		pass

	def test_get_LogEntry(self):
		pass



from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
@csrf_exempt
def endpoint(request: HttpRequest):
	data = json.loads(request.body)
	print(data)

	if("challenge" in data):
		return HttpResponse(data["challenge"])
	
	if("subscription" not in data or "status" not in data["subscription"] or data["subscription"]["status"] != "enabled"):
		return HttpResponseBadRequest()

	id = data["event"]["id"]
	uid = data["event"]["broadcaster_user_id"]
	t = data["event"]["type"]
	startedAt = data["event"]["started_at"]

	print((id, " ", uid, " ", t, " ", startedAt))
	return HttpResponse()
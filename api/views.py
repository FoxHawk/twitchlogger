from django.http.response import HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import loader
import json
from .. import manageSubscriptions

# Create your views here.

def fetchSubbedEvents(request: HttpRequest):
	pass

def fetchLogs(request: HttpRequest):
	pass
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import Template, loader

# Create your views here.

def index(request: HttpRequest):
	tp = loader.get_template("index.html")

	context = {"a":"b"}

	return HttpResponse(tp.render(context=context, request=request))

def manage(request: HttpRequest):
	pass
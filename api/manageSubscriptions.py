import requests
import json
from django.conf import settings

#client id and secret from twitch
clientID = settings.TWITCH_CLIENT_ID
clientSecret = settings.TWITCH_CLIENT_SECRET

bearerToken = None #will be set by getBearerToken()
url = "https://api.twitch.tv/helix/eventsub/subscriptions" #the url for all event subscriptions

def subscribeToAllEvents(channel: str):
	success = True

	if not subscribeToUpdateEvent(channel):
		success = False
	if not subscribeToOnlineEvent(channel):
		success = False
	if not subscribeToOfflineEvent(channel):
		success = False

	return success

def subscribeToUpdateEvent(channel: str):
	return subscribeToEvent(channel, "channel.update")

def subscribeToOnlineEvent(channel: str):
	return subscribeToEvent(channel, "stream.online")

def subscribeToOfflineEvent(channel: str):
	return subscribeToEvent(channel, "stream.offline")

def subscribeToEvent(channel: str, eventType: str):
	global bearerToken
	global url

	uid = getUserID(channel)
	if(not uid): #if we couldn't get the user's ID, return false
		return False

	#check if we have a bearer token already saved, if not, fetch one
	if (bearerToken == None and not getBearerToken()):
		return False #return false if we cannot get a bearer token

	body = {
	"type":eventType, "version":"1", "condition":{"broadcaster_user_id":uid}, "transport": {
		"method": "webhook", "callback": "https://twitch.foxhawk.co.uk/logger/endpoint", "secret": clientSecret}}

	#make the twitch api web request
	resp = requests.post(url, data=json.dumps(body), headers={"Client-ID": clientID, "Authorization": "Bearer " + bearerToken["access_token"], "Content-Type": "application/json"})

	if(resp.status_code == 409): #if the api returns error 409 conflict, the channel is already subscribed to, so return true
		return True

	if (not resp.ok): #if the api request returns an error code, return false
		return False

	response = json.loads(resp.text) #parse the response as json

	if("data" not in response or "status" not in response["data"][0]): #Check that the field "data" and "data.status" exist. if not, return false
		return False

	if(response["data"][0]["status"] == "webhook_callback_verification_pending"): #Check that the status is verification pending
		return True #return the id of the subscribed event
	return False

def unsubscribeFromAllEvents(channel: str):
	success = True

	if not unsubscribeFromOfflineEvent(channel):
		success = False
	if not unsubscribeFromOnlineEvent(channel):
		success = False
	if not unsubscribeFromUpdateEvent(channel):
		success = False
	
	return success

def unsubscribeFromUpdateEvent(channel: str):
	return unsubscribeFromEvent(channel, "channel.update")

def unsubscribeFromOnlineEvent(channel: str):
	return unsubscribeFromEvent(channel, "stream.online")
	
def unsubscribeFromOfflineEvent(channel: str):
	return unsubscribeFromEvent(channel, "stream.offline")

def unsubscribeFromEvent(channel: str, eventType: str):
	global bearerToken
	
	#check if we have a bearer token already saved, if not, fetch one
	if (bearerToken == None and not getBearerToken()):
		return False #return false if we cannot get a bearer token

	uid = getUserID(channel)
	if(not uid): #if we couldn't get the user's ID, return false
		return False
	
	#get the event ID used to unsunscribe from the event
	eventId = getEventFromID(uid, eventType)
	if(not eventId):
		return False #return false if we could not get the event id
	#send the http DELETE request to the twitch event endpoint
	resp = requests.delete(url, headers={"Client-ID": clientID, "Authorization": "Bearer " + bearerToken["access_token"]}, params={"id": eventId})

	if (not resp.ok):
		return False #if we do not get a 2xx response, return false
	
	return True #the unsubscription was a success


def getEventFromID(userID: str, eventType: str):
	events = getSubscribedEvents() #get a list of all subscribed events
	#search through the events for the one with the same user ID and event type
	for i in events:
		if (i["condition"]["broadcaster_user_id"] == userID and i["type"] == eventType):
			return i["id"] #return the event ID
	
	return False #return false if we can't find the right event

def getSubscribedEvents():
	global bearerToken

	#check if we have a bearer token already saved, if not, fetch one
	if bearerToken == None and not getBearerToken():
		return False #return false if we cannot get a bearer token

	events = []

	events, page = getEventListPage()

	while page != "":
		eventList, page = getEventListPage(page)
		events = events + eventList

	
	return events

def getEventListPage(after = ""):
	headers={"Client-ID": clientID, "Authorization": "Bearer " + bearerToken["access_token"]}
	events = []

	#send a get request to the twitch event subscription endpoint which returns a list of all events we are subscribed to
	resp = requests.get(url+ "?after=" + after, headers=headers)

	if not resp.ok: #if we do not get a 2xx response, return false
		return False
	
	data = json.loads(resp.text) #load the text into python objects
	
	if "data" not in data: #"data" is the top-level object in the json data we expect to get from twitch. if it isn't there, something went wrong
		return False
	#load all events into a more convenient format (remove the top-level "data" object)
	for i in data["data"]:
		events.append(i)
	
	if "cursor" in data["pagination"]:
		return events, data["pagination"]["cursor"]
	
	return events, ""


def getBearerToken():
	global bearerToken
	#send request to the twitch api to get a bearer token from our client ID and client secret
	resp = requests.post("https://id.twitch.tv/oauth2/token", params={"client_id": clientID, "client_secret": clientSecret, "grant_type": "client_credentials"})
	
	#parse returned body data as json. Check if the field "access_token" is included
	data = json.loads(resp.text)
	if("access_token" not in data):
		return False #return false if there isn't an access token in the response
	
	bearerToken = data #set the global variable with the json data (dict)
	return True

def getUserID(channel: str):
	global bearerToken

	#check if we have a bearer token already saved, if not, fetch one
	if (bearerToken == None and not getBearerToken()):
		return False #return false if we cannot get a bearer token

	#send request to twitch api endpoint to get user info
	resp = requests.get("https://api.twitch.tv/helix/users", params={"login": channel}, headers={
		"Client-ID": clientID, "Authorization": "Bearer " + bearerToken["access_token"]})
	#if the api did not respond with code 200 then return false
	if (resp.status_code != 200):
		return False
	
	#parse response body as json
	data = json.loads(resp.text)
	#if the fields "data" and "data.id" exist, return the user id
	if("data" in data and "id" in data["data"][0]):
		return data["data"][0]["id"]
	
	return False #if the fields do not exist, return false

def getUserData(userID: str):
	global bearerToken

	#check if we have a bearer token already saved, if not, fetch one
	if (bearerToken == None and not getBearerToken()):
		return False #return false if we cannot get a bearer token

	resp = requests.get("https://api.twitch.tv/helix/users/", params={"id": userID}, headers={
		"Client-ID": clientID, "Authorization": "Bearer " + bearerToken["access_token"]})
	
	if (resp.status_code != 200):
		return False
	
	data = json.loads(resp.text)["data"][0]

	return data

def getChannelData(userID: str):
	global bearerToken

	#check if we have a bearer token already saved, if not, fetch one
	if (bearerToken == None and not getBearerToken()):
		return False #return false if we cannot get a bearer token

	resp = requests.get("https://api.twitch.tv/helix/channels/", params={"broadcaster_id": userID}, headers={
		"Client-ID": clientID, "Authorization": "Bearer " + bearerToken["access_token"]})
	
	if (resp.status_code != 200):
		return False
	
	data = json.loads(resp.text)["data"][0]

	return data

if __name__ == "__main__":
	unsubscribeFromAllEvents("digitalvagrant")
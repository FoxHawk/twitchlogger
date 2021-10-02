import requests
import json
import copy

#client id and secret from twitch
clientID = "768qvzzen9xh7ed1nzp2xzngcealc1"
clientSecret = "7zktl2y9jf9dutnxccir19fqek44xg"

bearerToken = None #will be set by getBearerToken()
url = "https://api.twitch.tv/helix/eventsub/subscriptions"

#template for the subscribe request body
subscribeTemplate = {
	"type":"stream.online", "version":"1", "condition":{"broadcaster_user_id":"0"}, "transport": {
		"method": "webhook", "callback": "https://twitch.foxhawk.co.uk/logger/endpoint", "secret": clientSecret}}

def subscribeToChannel(channel: str):
	global bearerToken
	global url

	#check if we have a bearer token already saved, if not, fetch one
	if (bearerToken == None and not getBearerToken()):
		return False #return false if we cannot get a bearer token

	uid = getUserID(channel)
	if(not uid): #if we couldn't get the user's ID, return false
		return False
	#create a copy of the subscribe template and fill in the user id
	body = copy.deepcopy(subscribeTemplate)
	body["condition"]["broadcaster_user_id"] = uid
	#make the twitch api web request
	resp = requests.post(url, data=json.dumps(body), headers={"Client-ID": clientID, "Authorization": "Bearer " + bearerToken["access_token"], "Content-Type": "application/json"})

	if (not resp.ok): #if the api request returns an error code, return false
		return False

	response = json.loads(resp.text) #parse the response as json

	if("data" not in response or "status" not in response["data"][0]): #Check that the field "data" and "data.status" exist. if not, return false
		return False

	if(response["data"][0]["status"] == "webhook_callback_verification_pending"): #Check that the status is verification pending
		return response["data"][0]["id"] #return the id of the subscribed event

def unsubscribeFromChannel(channel: str):
	global bearerToken
	
	#check if we have a bearer token already saved, if not, fetch one
	if (bearerToken == None and not getBearerToken()):
		return False #return false if we cannot get a bearer token

	uid = getUserID(channel)
	if(not uid): #if we couldn't get the user's ID, return false
		return False
	
	eventId = getEventFromID(uid)
	if(not eventId):
		return False
	
	resp = requests.delete(url, headers={"Client-ID": clientID, "Authorization": "Bearer " + bearerToken["access_token"]}, params={"id": eventId})

	if (not resp.ok):
		return False
	
	return True


def getEventFromID(userID: str):
	events = getSubscribedEvents()

	for i in events:
		if (i[1] == userID):
			return i[0]
	
	return False

def getSubscribedEvents():
	global bearerToken

	#check if we have a bearer token already saved, if not, fetch one
	if (bearerToken == None and not getBearerToken()):
		return False #return false if we cannot get a bearer token

	resp = requests.get(url, headers={"Client-ID": clientID, "Authorization": "Bearer " + bearerToken["access_token"]})
	
	if (not resp.ok):
		return False
	
	data = json.loads(resp.text)
	
	if ("data" not in data):
		return False

	eventIDs = []

	for i in data["data"]:
		eventIDs.append((i["id"], i["condition"]["broadcaster_user_id"]))
	
	return eventIDs

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
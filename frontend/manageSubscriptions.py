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
	resp = requests.post(url, data=body, headers={"Client-ID": clientID, "Authorization": "Bearer " + bearerToken["access_token"], "Content-Type": "application/json"})

	if (resp.status_code != 200): #if the api request doesn't give a 200 response, return false
		return False

	response = json.loads(resp.text) #parse the response as json

	if("data" not in response or "status" not in response["data"]): #Check that the field "data" and "data.status" exist. if not, return false
		return False

	if(response["data"]["status"] == "webhook_callback_verification_pending"): #Check that the status is verification pending
		return response["data"]["id"] #return the id of the subscribed event

def unsubscribeFromChannel(channel: str):
	global bearerToken
	global url
	
	#try to get the uid of the user. if we can't, return false
	uid = getUserID(channel)
	if(not uid):
		return False
	#send a delete request to the twitch api
	resp = requests.delete(url, headers={"Client-ID": clientID, "Authorization": "Bearer " + bearerToken["access_token"]}, params={"id": uid})

	return resp.status_code == 200 #return whether the response code was 200 or not (true or false respectively)

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
	#send request to twitch api endpoint to get user info
	resp = requests.get("https://api.twitch.tv/helix/streams", params={"user_login": channel})
	#if the api did not respond with code 200 then return false
	if (resp.status_code != 200):
		return False
	
	#parse response body as json
	data = json.loads(resp.text)
	#if the fields "data" and "data.user_id" exist, return the user id
	if("data" in data and "user_id" in data["data"]):
		return data["data"]["user_id"]
	
	return False #if the fields do not exist, return false

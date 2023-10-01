from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
load_dotenv() #client variables stored in enviornment file
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
#backend projects only need client_id and client_secret
#first need to request access token to access api, done by sending client_id, client_secret and grant_type
#access token returned (with 10 minute expiry)
#once access is given, requests can be given to API
#api returns data
#if token expires new token is needed
#grant_type needed to state that it is client_credentials, so only specifying that client_id etc is needed
def get_token():
    auth_string = client_id + ":" + client_secret #authorization string needs to be this format
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8") #returns base_64 object as string
    url = "https://accounts.spotify.com/api/token" #url that auth_string will be sent to
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data) #returned as json
    json_result = json.loads(result.content) #convert json to dictionary
    token = json_result["access_token"] #get access token from json object
    return token
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}
def artist_search(token, artist_name):
    url = "https://api.spotify.com/v1/search" #api used to search for artist (or tracks)
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1" #use &type=artist,track to search for artist and a track, limit = 1 will only get most popular artist
    query_url = url + query #fstrings are string formating
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        return None
    return json_result[0]

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=UK" #finds top tracks by this artist
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

token = get_token()
artist_name = "ACDC"
result = artist_search(token, artist_name)
artist_id = result["id"]
songs = get_songs_by_artist(token, artist_id)
print(songs)

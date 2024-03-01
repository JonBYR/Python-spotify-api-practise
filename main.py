from dotenv import load_dotenv #to install this use pip install python-dotenv
import os #tutorial used https://www.youtube.com/watch?v=WAmEZBEeNmg
import base64
from requests import post, get
import json
load_dotenv() #client variables stored in enviornment file
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
artist_name = input("Please enter an artist: ")
artist_song = input("Please input this artists song: ")
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
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8") #returns base_64 object as string, the object type that spotify requests

    url = "https://accounts.spotify.com/api/token" #url that auth_string will be sent to, in order to request access token
    headers = { #headers required to be sent to spotify to get token
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"} #grant type for access token
    result = post(url, headers=headers, data=data) #returned as json, allows to sent post request
    json_result = json.loads(result.content) #convert json to dictionary, result is returned as .content
    token = json_result["access_token"] #get access token from json object
    return token
def get_auth_header(token): #function for api requests
    return {"Authorization": "Bearer " + token}
def get_track_id(token, artist, song):
    url = "https://api.spotify.com/v1/search" #api used to search for artist (or tracks)
    headers = get_auth_header(token)
    query = f"?q={artist}, {song}&type=artist,track&limit=1" #use &type=artist,track to search for artist and a track, limit = 1 will only get most popular song
    query_url = url + query #fstrings are string formating to create a query in the spotify api, ? needed at start of query string
    result = get(query_url, headers=headers) #format the information is returned as 
    json_result = json.loads(result.content)["tracks"]["items"] #converts this into a dictionary and gets these two headers 
    if len(json_result) == 0:
        return None
    return json_result[0] #returns the first element of the dictionary file
def get_track_information(token, id):
    url = f"https://api.spotify.com/v1/audio-analysis/{id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result #returns all information from get_track_audio_analysis as a json file, could try and do return json_result[1] to try and return only the track header in the file
token = get_token()
result_track = get_track_id(token,artist_name,artist_song)
song_id = result_track["id"] #dictionary is returned and id is stored from the id key field
track_info = get_track_information(token, song_id)
track = track_info["track"] #stores all information relating to the track tag in the json object
with open('musicdata.json', 'w') as exportFile: #writes all the track_information returned from spotify into a json file using the dump method
    json.dump(track, exportFile)

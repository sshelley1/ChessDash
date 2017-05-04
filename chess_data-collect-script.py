# --------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                                                                                                   #
#   Python Script - GeoLocation                                                                                                                     #
#                                                                                                                                                   #
#   By Saad Khan, Scott Shelley, Lamonte Carter                                                                                                     #
#                                                                                                                                                   #
#   The purpose of the following python script is to soley generate Geo Coordinates from twitter into Kibana which will be used to print            #
#       Coordinates into a tile map. All the data here goes to localhost and is printed into JSON/ElasticSearch for the visuals.                    #
#       Our project is focused on Chess, but this script can be used for any data really. Based on findings, people can hide their Geo Coordinates  #
#       so the code seperates the data into 2 locations for kibana to read seperately: one location is for geocoordinates given by the user and     #
#       other one is for string location data where users can input garbage data such as "The Sun" as location. We seperate the data into 2         #
#       because if gives a more accurate representation of locations since the data can be heavily affected by users declining to give coordinates  #
#                                                                                                                                                   #
#   *Important note - Execute the "JsonMapping file within Kibana before importing the data from this script,                                       #
#       or else the formating will be heavily affected                                                                                              #
#                                                                                                                                                   #
# --------------------------------------------------------------------------------------------------------------------------------------------------#

#   Importing Libraries
import json
import requests
import tweepy
import elasticsearch
#   The following Acess Token/keys are used to confirm and authorize Tweepy for it's API
ACCESS_TOKEN = '793829198112501760-41cDNkTYIlAtueTlVeVFnNTvAYd4aN1'
ACCESS_SECRET = 'weEGrhmG7doH4dwIbDtMYAcjTllWOoUla5KhDWkP88doZ'
CONSUMER_KEY = 'UliqTh4cO7UZyIYsXN2wtZdyw'
CONSUMER_SECRET = 'kcLRRCC1lVUIrXfLckS4eQsokTzW2ryj5f1z80Gsv5fWzeVkmp'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

#   Json data is printed onto this body
body_json={'tweeters': []}
#   Variables are initialized here
handle = ''
followers = 0
location = ''
#   i variable is used as an index/count variable for all the results
i=0
#   The following Loop is used for searching and pasting search results for chess into the json body
for x in tweepy.Cursor(api.search, q='chess', rpp=5, count= 10000, result_type="recent", since = '2010-04-01',until ='2017-05-01', include_entities=True, lang="en").items(10000):
    i+=1
    handle = x.user.screen_name
    followers = x.user.followers_count
    location = x.user.location
    geo_point = x.coordinates
#   The code bellow is used to sort data that has geo coordinates and data without geo coordinates
    a = None;
    if not geo_point is None:       #   By default it sets coordinates to none and if the If statement doesn't import geopoints to the coordinates
        a=geo_point['coordinates']  #       the next if statment will sort it out      
    if not a is None:
        try:
            print(x.user.screen_name,x.user.followers_count,x.coordinates)
            # This is where the json file is printed onto, important to keep note of this location "chess_geocoord" for Kibana to read 
            url = "http://localhost:9200/chess_geocoord/chesstype/"+ str(i)
            # This is the formating of the data
            geodata = { 'handle': x.user.screen_name ,'followers': x.user.followers_count, 'geo_point': a}    
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.post(url, data=json.dumps(geodata), headers=headers)
            print(geodata)     # this is here to show the user who is executing the python script to see what data is comming in
            print(r)
        except UnicodeError:    #   We found that users could put Non-BMP characters into their data so this try/catch/except statement is here to ignore data with no support
            continue
    else:
        try:
            print(x.user.screen_name,x.user.followers_count,x.user.location)
            # This is where the json file is printed onto, important to keep note of this location "chess_non_geocoord" for Kibana to read 
            url = "http://localhost:9200/chess_non_geocoord/chesstype/"+ str(i)
            # This is the formating of the data
            non_geodata = { 'handle': x.user.screen_name ,'followers': x.user.followers_count, 'location': x.user.location}   
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.post(url, data=json.dumps(non_geodata), headers=headers)
            print(non_geodata)     # this is here to show the user who is executing the python script to see what data is comming in
            print(r)
        except UnicodeError:    #   We found that users could put Non-BMP characters into their data so this try/catch/except statement is here to ignore data with no support
            continue
    
    
print (i)

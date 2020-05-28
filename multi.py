import json
import re
import http.client
import argparse
from bs4 import BeautifulSoup
import random

##func to get setlists
def getShow(show_type):
	conn = http.client.HTTPSConnection("api.phish.net")
	payload = "{}"
	conn.request("GET", show_type, payload)
	res = conn.getresponse()
	data = res.read()

	json_string = data.decode("utf-8")
	parsed_json = json.loads(json_string)
	return parsed_json

###Get API Key
fo = open("api.txt","r")
apikey = fo.read()
fo.close()
callhome = True
########################

parser = argparse.ArgumentParser(description='Welcome to Tacklebox!')
parser.add_argument("--song", default=None, type=str)

args = parser.parse_args()


##Below is what I have to put into a function into Tacklebox
show_type = '/v3/jamcharts/all?apikey=' + apikey 
setlist = getShow(show_type)
songs = setlist["response"]["data"]   

for x in range(0,len(songs)-1):
    if songs[x]["song"] == args.song:
        songid = songs[x]["songid"]

show_type = '/v3/jamcharts/get?apikey=' + apikey + '&songid=' + str(songid)
jamchart = getShow(show_type)
jamchart = jamchart["response"]["data"]["entries"]
print("There are " + str(len(jamchart)) + " Jamchart entries for " + args.song + ".")
x = random.randrange(0,len(jamchart)-1)
print(jamchart[x]["showdate"])
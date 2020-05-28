import json
import re
import http.client
import argparse
from bs4 import BeautifulSoup

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
parser.add_argument("--pull", action="store_true")
parser.add_argument("--song", default=None, type=str)

args = parser.parse_args()

show_type = '/v3/jamcharts/all?apikey=' + apikey 

if args.pull == True:
    setlist = getShow(show_type)
    f = open("multi.json","w+")
    json.dump(setlist, f)
    f.close()
else:
    fo = open("multi.json","r")
    setlist_base = fo.read()
    setlist = json.loads(setlist_base)
    fo.close

print(args.pull)
print(args.song)
print(setlist)
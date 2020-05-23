#Tacklebox
#A nerdy diversion using the phish.net API
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

def pretty_up(bad_string):
	bad_string = re.sub('Set 1: ', '\nSet 1: ',bad_string)
	bad_string = re.sub('Set 2: ', '\nSet 2: ',bad_string)
	bad_string = re.sub('Set 3: ', '\nSet 3: ',bad_string)
	bad_string = re.sub('Encore: ', '\nEncore: ',bad_string)
	return bad_string

def displaySetlist(sl_text):
	encore = sl_text[sl_text.find('Encore: '):]
	notes = encore[encore.find('[1] '):]
	sl_text = sl_text[0:sl_text.find('Encore: ')]
	encore = encore[0:encore.find('[1] ')]
	sl_text = sl_text + encore + '\n' + notes
	return sl_text

###Get API Key
fo = open("api.txt","r")
apikey = fo.read()
fo.close()
callhome = True
#########################################

###set up arguments
parser = argparse.ArgumentParser(description='Welcome to Tacklebox!')
parser.add_argument("--date", default="1900-01-01")
parser.add_argument("--previous", action="store_true")
parser.add_argument("--latest", action="store_true")
args = parser.parse_args()
#########################################

if args.previous == True:
	callhome = False

if args.date == '1900-01-01':
	show_type = '/v3/setlist/random?apikey=' + apikey 
else:
	show_type = '/v3/setlists/get?apikey=' + apikey + '&showdate=' + args.date

if args.latest == True:
	show_type = '/v3/setlists/latest?apikey=' + apikey

if callhome == True:
	setlist = getShow(show_type)
else:
	fo = open("setlist.json","r")
	setlist_base = fo.read()
	setlist = json.loads(setlist_base)
	fo.close


sl_text = pretty_up(BeautifulSoup(setlist["response"]["data"][0]["setlistdata"],"html.parser").text)

print("Show Date: " + setlist["response"]["data"][0]["showdate"])
print("Venue: " + BeautifulSoup(setlist["response"]["data"][0]["venue"],"html.parser").text)
print("Location: " + BeautifulSoup(setlist["response"]["data"][0]["location"],"html.parser").text)
print("Setlist: " + displaySetlist(sl_text))
print("Notes: " + BeautifulSoup(setlist["response"]["data"][0]["setlistnotes"],"html.parser").text)
print("Phish.in link: http://phish.in/" + setlist["response"]["data"][0]["showdate"])

if callhome == True:
	f = open("setlist.json","w+")
	json.dump(setlist, f)
	f.close()
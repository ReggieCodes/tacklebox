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

##since we're not a webpage we have to do some cleanup on the setlist string
def displaySetlist(sl_text):
	sl_text = re.sub('Set 1: ', '\nSet 1: ',sl_text)
	sl_text = re.sub('Set 2: ', '\nSet 2: ',sl_text)
	sl_text = re.sub('Set 3: ', '\nSet 3: ',sl_text)
	sl_text = re.sub('Encore: ', '\nEncore: ',sl_text)
	encore = sl_text[sl_text.find('Encore: '):]
	
	if encore.find('[1] ') == -1:
		notes = ''
	else:
		notes = encore[encore.find('[1] '):]
	
	sl_text = sl_text[0:sl_text.find('Encore: ')]
	if encore.find('[1] ') != -1 :
		encore = encore[0:encore.find('[1] ')]
		
	sl_text = sl_text + encore + '\n' + notes
	return sl_text

##Make a way to clean up the notes in case some of them are a little squirrley
def displayNotes(sl_notes):
	sl_notes = re.sub('\nvia phish.net','via phish.net',sl_notes) #some setlists have the newline, so remove those that do
	sl_notes = re.sub('via phish.net','\nvia phish.net',sl_notes)
	return sl_notes

##Check JEMP for if Phish is playing
def jemp():
	jemp_conn = http.client.HTTPSConnection("public.radio.co")
	station = 'stations/sd71de59b3/status'
	payload = "{}"
	jemp_conn.request("GET", station, payload)
	res = jemp_conn.getresponse()
	data = res.read()

	json_string = data.decode("utf-8")
	now_playing = json.loads(json_string)

	print("JEMP is currently playing: " + now_playing["current_track"]["title"])
	song = now_playing["current_track"]["title"]

	artist = song[0:7]
	showdate = song[song.find("(")+1:song.find(")")]

	if artist == 'Phish -':
		print("Phish is playing!")
		if int(showdate[-2:]) < 80:
			year = str(int(showdate[-2:]) + 2000)
		else:
			year = str(int(showdate[-2:]) + 1900)

		month = showdate[:-3]
		month = "000" + month[:month.find("-")]
		month = month[-2:]
		day = showdate[:-3]
		day = "000" + day[day.find("-")+1:]
		day = day[-2:]
		show = year + "-" + month + "-" + day
	else:
		print("Phish is not playing :(")
		show = "1900-01-01"

	return(show)

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
parser.add_argument("--jemp",action="store_true")
parser.add_argument("--tiph",action="store_true")
parser.add_argument("--progress",action="store_true")
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

if args.tiph == True:
	show_type = '/v3/setlists/tiph?apikey=' + apikey

if args.progress == True:
	show_type = '/v3/setlists/progress?apikey=' + apikey

if args.jemp == True:
	showdate = jemp()
	if showdate == '1900-01-01':
		print("Since Phish isn't playing here's the last show you got:")
		callhome = False
	else:
		show_type = '/v3/setlists/get?apikey=' + apikey + '&showdate=' + showdate

if callhome == True:
	setlist = getShow(show_type)
else:
	fo = open("setlist.json","r")
	setlist_base = fo.read()
	setlist = json.loads(setlist_base)
	fo.close

sl_text = BeautifulSoup(setlist["response"]["data"][0]["setlistdata"],"html.parser").text
sl_notes = BeautifulSoup(setlist["response"]["data"][0]["setlistnotes"],"html.parser").text

print("Show Date: " + setlist["response"]["data"][0]["showdate"])
print("Venue: " + BeautifulSoup(setlist["response"]["data"][0]["venue"],"html.parser").text)
print("Location: " + BeautifulSoup(setlist["response"]["data"][0]["location"],"html.parser").text)
print("\nSetlist: " + displaySetlist(sl_text))
print("\nNotes: " + displayNotes(sl_notes))
print("\nPhish.in link: http://phish.in/" + setlist["response"]["data"][0]["showdate"])

if callhome == True:
	f = open("setlist.json","w+")
	json.dump(setlist, f)
	f.close()
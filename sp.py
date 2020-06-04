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

show_type = '/v3/shows/query?apikey=' + apikey + '&order=ASC&artistid=9'
setlist = getShow(show_type)
i = int(setlist["response"]["count"])
projects = []
showids = []
artist = "Page"

for x in range(i):
    if setlist["response"]["data"][x]["billed_as"] not in projects:
        projects.append(setlist["response"]["data"][x]["billed_as"])

print(artist + "has played in the following bands, choose one:")

z = 0
while z < len(projects):
    print(str(z) + ". - " + projects[z])
    z += 1

z = int(input("? "))

for x in range(i):
    if setlist["response"]["data"][x]["billed_as"] == projects[z]:
        showids.append(setlist["response"]["data"][x]["showid"])

i = len(showids)
i = random.randrange(0,i-1)
var = show_type = '/v3/setlists/get?apikey=' + apikey + '&showid=' + str(showids[i])
print(var)
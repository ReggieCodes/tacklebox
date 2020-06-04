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

def sideProjects(artist_name, artist_id):
	show_type = '/v3/shows/query?apikey=' + apikey + '&order=ASC&artistid=' + artist_id
	setlist = getShow(show_type)
	i = int(setlist["response"]["count"])
	projects = []
	showids = []

	for x in range(i):
		if setlist["response"]["data"][x]["billed_as"] not in projects:
			projects.append(setlist["response"]["data"][x]["billed_as"])

	print(artist_name + "has played in the following bands, choose one:")

	z = 0
	while z < len(projects):
		print(str(z) + ". " + projects[z])
		z += 1

	z = 420
	while True:
		z = input("? ")

		try:
			z = int(z)
		except ValueError:
			z = 420

		if z >= 0 and z <= (len(projects)-1):
			break
		else:
			print("Please input a valid # in the list above.")

	for x in range(i):
		if setlist["response"]["data"][x]["billed_as"] == projects[z]:
			showids.append(setlist["response"]["data"][x]["showid"])

	i = len(showids)
	if i == 1:
		var = show_type = '/v3/setlists/get?apikey=' + apikey + '&showid=' + str(showids[0])
	else:
		i = random.randrange(0,i-1)
		var = show_type = '/v3/setlists/get?apikey=' + apikey + '&showid=' + str(showids[i])
	return(var)


###Get API Key
fo = open("api.txt","r")
apikey = fo.read()
fo.close()
callhome = True
########################

show_type= sideProjects("Page","9")
print(show_type)
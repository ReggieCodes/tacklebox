import json
import http.client

conn = http.client.HTTPSConnection("public.radio.co")
station = 'stations/sd71de59b3/status'
payload = "{}"
conn.request("GET", station, payload)
res = conn.getresponse()
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

print(show)
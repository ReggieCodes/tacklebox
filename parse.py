import requests
from bs4 import BeautifulSoup

html = requests.get("https://phish.net/setlists/page-mcconnell-april-12-1999-club-front-san-rafael-ca-usa.html")
soup = BeautifulSoup(html.content, "html.parser")
setlist = soup.find(class_="setlist-container sideshow sideshow-9")
#setlist = BeautifulSoup(setlist,"html.parser")
print(setlist)
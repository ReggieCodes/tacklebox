# Tacklebox

This is a python script to give you a CLI for accessing the phish.net API.

## Requirements

1. This was developed in Python 3.7.4
2. You need a phish.net API key.  If you have an account on .net these are free, just go to <https://api.phish.net/keys/> and sign up for one.  Once you have your key, put it in a text file named api.txt in the same directory as the script.
3. You will need to get Beautiful Soup 4.  This can be done via pip:

    pip install beautifulsoup4

## How to use

If you just run the following command, it will return a random setlist:

    python tacklebox.py
There is the --latest flag that will return the most recent Phish show:

    python tacklebox.py --latest
The --date flag can bring back a specific show.  Dates need to be formatted as YYYY-MM-DD. Example below:

    python tacklebox.py --date=2000-06-24
The --previous flag will bring back the last show returned by Tacklebox.

    python tacklebox.py --previous
The --jemp flag will check to see what's playing on JEMP Radio and if it's Phish it will bring back the setlist for the entire show.

    python tacklebox.py --jemp

## To do

1. I'm sure there are some bugs and oddities.  As I find them I will fix them.
2. JEMP seems to work fine for individual shows, might need to add different parsing for full shows.
3. I might add some more flags for different API calls as I dig into it more, like the "Today in history" call.

### Thank you for looking at my project and I hope it inspires you to do your own.  Enjoy the music

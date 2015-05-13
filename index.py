from os import listdir
from os.path import isfile, join
import time
from elasticsearch import Elasticsearch 


def get_artist_title(f):
    artist, operator, title = f.partition("__")
    artist = reformat(artist)
    title = reformat(title)
    return (artist, title)

def reformat(str):
    new_str = ""
    for i in str.split("_"):
        if len(i) > 1:
            new_str = new_str + i[0] + i[1:].lower() + " "
        else:
            new_str = new_str + i

    new_str = new_str.replace("Lyrics.txt", "")

def get_lyric(f):
    try:
        fp = open(f, 'r')
        lyric_dirty = fp.read()
    except:
        print "Error reading file"

    lyric = fp.read()
    return lyric

folder = "./lyrics/"
files = [ folder+f for f in listdir(folder) ]

for f in files:
    artist, title = get_artist_title(f)
    lyric = get_lyric(f)

    time.sleep(1)


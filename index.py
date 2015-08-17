from os import listdir
from os.path import isfile, join
import time
import json 
from collections import Counter
import subprocess

def split():
    line_counter = 0;
    file_counter = 0;
    big_file = open("jsonFile.txt", "r")

    small_file = open("json_" + str(file_counter), "w")

    for line in big_file:
        small_file.write(line)
        line_counter = line_counter + 1
        if line_counter % (31840/2) == 0:
            small_file.close()
            file_counter = file_counter + 1;
            small_file = open("json_" + str(file_counter), "w")
    big_file.close()

def curl():
    start_time = time.time()
    subprocess.call('curl -s -XPOST localhost:9200/_bulk --data-binary @jsonFile.txt; echo',shell = True)
    print("--- %s seconds ---" % (time.time() - start_time))
    #for i in xrange(2):
    #   subprocess.call('curl -s -XPOST localhost:9200/_bulk --data-binary @json_'+str(i)+'; echo',shell = True)
    #   time.sleep(.1)
    print("--- %s seconds ---" % (time.time() - start_time))



def get_artist_title(f):
    artist, operator, title = f.partition("__")
    artist = reformat(artist)
    artist = artist[9:]
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
    return new_str

def get_lyric(f):
    try:
        fp = open(f, 'r')
        lyric = fp.read()
        # escape all the new-line chars
        lyric = lyric.replace("\n", "")
        return lyric
    except:
        print "Error reading file"



def readwords( filename ):
    f = open(filename)
    words = [ line.rstrip() for line in f.readlines()]
    return words

folder = "./lyrics/"
files = [ folder+f for f in listdir(folder) ]

output = open('jsonFile.txt', 'w')

for i,f in enumerate(files):
    artist, title = get_artist_title(f)
    lyric = get_lyric(f)   
    lyric = ''.join(lyric.splitlines())

    positive = readwords('./positive.txt')
    negative = readwords('./negative.txt')

    count = Counter(lyric.split())

    pos = 0
    neg = 0

    for key, val in count.iteritems():
        key = key.rstrip('.,?!\n') # removing possible punctuation signs
        if key in positive:
            pos += val
        if key in negative:
            neg += val

    song_sentiment = pos-neg

    if (song_sentiment >= 0):
        song_des = "positive"
    else: song_des = "negative"

    #try:
    output.write('{ "create": { "_index": "snagy_index", "_type": "doc"}}\n')
    output.write('{"doc_id": "'+str(f)+'", "artist" : "'+artist+'", "title" : "'+title+'", "body" : "'+lyric+'", "sentiment" : "'+song_des+'", "score" : "'+str(song_sentiment)+'" }\n')
    #except:
    #    try: 
    #        print "Can't do this" + str(i) + " " + artist + " " + title + " " + lyric
    #    except:
    #        print "Hell no" + str(i)
    

curl()

output.close()

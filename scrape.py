# Lo and Behold the world's worst code ever written

from bs4 import BeautifulSoup
import urllib2
import time
import os
import threading
import pyprind

url = "http://www.songlyrics.com"

lyrics = urllib2.urlopen("http://www.songlyrics.com/z/")
soup = BeautifulSoup(lyrics)

# get all of the lyrics
pages = soup.find("ul", {'class':'pagination'}).findAll("li", attrs = {'class':'li_pagination'})
# get rid of the first and last index, which both point to the first pages
pages = pages[1:-1]
#print len(pages)
def scrape(start, fin, thread_ind):
	links = []
	for i in range(start,fin):
		link = pages[i].find("a")["href"]
		links.append(link)

	for link in links:
		try:
			cur_page = urllib2.urlopen(url+link)
			page_soup = BeautifulSoup(cur_page)
		except: 
			print "URL Error from first-loop"
			continue

		for lyric_row in page_soup.find("tbody").findAll("td", attrs={'width':'70%'}):
			try:
				artist_page = urllib2.urlopen(lyric_row.find("a")["href"])
				artist_soup = BeautifulSoup(artist_page)
			except: 
				print "URL Error from artist-loop"
				continue

			for song_row in artist_soup.find("tbody").findAll("td", attrs={'width':'93%'}): 
				try:
					lyric_page = urllib2.urlopen(song_row.find("a")["href"])
					lyric_soup = BeautifulSoup(lyric_page)
					lyric = lyric_soup.find("p", attrs = {'id':'songLyricsDiv'}).get_text().replace('\n', ' ')
				except:
					print "Lyric Error"
					continue
				# the following line was taken from stackoverflow...i didn't want to waste a lot of time using loops, so i would just chain them together
				title = lyric_soup.title.get_text().replace("(", "").replace(")", "").replace(".", "").replace("-", "").replace("/", "").replace(" ", "_")
				path = "./lyrics/" + title + ".txt"
				f = open(path, 'w')

				try: 
					f.write(lyric)
				except: 
					print "Can't be written!"
					os.remove(path)

				print ("Finshed printing %s") % title
				f.close()
				
				time.sleep(0.2)
	return


''' 
	Since we're dealing with a lot of data, we're going to spin up 5 threads to scrape 
	different portions of the site concurrently
'''
# define the number of threads and the number of pages each thread is going to access
threads = []
num_threads = 3
num_pages = len(pages)/num_threads

for i in range(num_threads):
	start= i*num_pages
	end = start + num_pages
	thread = threading.Thread(target=scrape, args=(start,end,i,))
	threads.append(thread)
	thread.start()

for thread in threads: 
	thread.join() 

os.system('say "Scraping is done"')

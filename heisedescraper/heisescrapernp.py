#Code written by Rainier Robles for use in a course assignment for Database Systems at Freie Universität Berlin
#In the event that code is taken/adapted from an existing source, the sources are attributed in the comments

# imports
from bs4 import BeautifulSoup
import requests
import re #for Regular Expressions
import numpy as np #for Numerical Python, so we can count entries without hardcoding a loop

def getPage(url):
	"""
	Function takes a url and returns a soup page object. Copied from the Greyhound scraper at https://github.com/xconnect/fub.bsc.dbs.scraper.greyhound-data.com .
	"""
	r = requests.get(url)
	data = r.text
	spobj = BeautifulSoup(data, "lxml")
	return spobj

def getHeaders(content):
	"""
	Function takes some content, parses the article headers and adds them to a list, parses the words in the article headers, converts them to lowercase, then finally adds them to our word list. 
	"""
	for c in content:
		if c.header != None:
			allheaders.append((c.header).string.strip())

	for header in allheaders:
		words = re.findall("[\w'-]+", header)
		for word in words:
			madelower = word.lower()
			allwords.append(madelower)

#initialise variables
heiseurl = "https://www.heise.de/thema/https?seite=" #URL of the website
allheaders = [] #all headlines
allwords = [] #all words in the headlines
zippedwordcount = [] #tuples of words in the headlines and how often they're  used in headlines

page = 0
while True:
	zuoeffnen = heiseurl+str(page)
#	print("Opening "+zuoeffnen) #for testing purposes only, in order to identify sources of errors
	content = getPage(zuoeffnen).find("div", { "class" : "keywordliste" })
	if content == None: #loop ends when no <div class="keywordliste"> tag is found
		break
	content = content.findAll("div")
	getHeaders(content)
	page += 1

sortedwords = sorted(allwords) #sorts our word list

#counts how often a word is used in the headlines, places it in a tuple, and saves all tuples into a list
word, count = np.unique(sortedwords, return_counts=True)
zippedwordcount = list(zip(list(word),list(count)))

#Tuples are sorted in a descending order by how often they're used in headlines. Source: https://stackoverflow.com/questions/14466068/sort-a-list-of-tuples-by-second-value-reverse-true-and-then-by-key-reverse-fal
sortedcounts = sorted(zippedwordcount,key=lambda x:(-x[1],x[0]))

#prints out the ten most-used words
print("Top 10 Wörter:")
for i in range(0,10):
	print(sortedcounts[i][0]+"\t\t\t"+str(sortedcounts[i][1]))
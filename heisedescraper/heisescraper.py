# imports
from bs4 import BeautifulSoup
import requests
import re #für Regular Expressions

def getPage(url):
	"""
	Function takes a url and returns a soup page object. Copied from the Greyhound scraper.
	"""
	r = requests.get(url)
	data = r.text
	spobj = BeautifulSoup(data, "lxml")
	return spobj

def getHeaders(content):
	"""
	Function takes some content, parses the article headers and adds them to a list,  parses the words in the article headers, converts them to lowercase, then finally adds them to our word list. 
	"""
	for c in content:
		if c.header != None:
			allheaders.append((c.header).string.strip())

	for header in allheaders:
		words = re.findall("[\w'-]+", header)
		for word in words:
			madelower = word.lower()
			allwords.append(madelower)

#initialisiert Variablen
heiseurl = "https://www.heise.de/thema/https?seite=" #URL der Seiten
allheaders = [] #alle Überschriften
allwords = [] #alle Wörter in Überschriften
zippedwordcount = [] #Tupeln von Wörter und wie oft die in Überschriften verwendet werden

page = 0
while True:
	zuoeffnen = heiseurl+str(page)
#	print("Opening "+zuoeffnen) #nur zum Testen, damit wissen wir, woher den Fehler kommt
	content = getPage(zuoeffnen).find("div", { "class" : "keywordliste" })
	if content == None: #Schleife hört auf, wenn kein <div class="keywordliste"> Tag gefunden wird
		break
	content = content.findAll("div")
	getHeaders(content)
	page += 1

sortedwords = sorted(allwords) #sortierte Liste von Wörter

#zählt wie oft ein Wort in Überschriften benutzt wird, zipped das Wort mit der Anzahl in einem Tupel, und speichert die in einer Liste
i = 0
while i < len(sortedwords):
	j = i+1
	word = sortedwords[i]
	zaehler = 1
	while j < len(sortedwords) and word == sortedwords[j] :
		zaehler+=1
		j+=1
	zippedwordcount.append((zaehler,word))
	i=j

#Quelle für die Sortierung: https://stackoverflow.com/questions/14466068/sort-a-list-of-tuples-by-second-value-reverse-true-and-then-by-key-reverse-fal
sortedcounts = sorted(zippedwordcount,key=lambda x:(-x[0],x[1]))

#gibt Top 10 benutzte Wörter zurück
#Merke: https ist kein Wort der deutschen Sprache!
print("Top 10 Wörter:")
for i in range(0,10):
	print(sortedcounts[i][1]+"\t\t\t"+str(sortedcounts[i][0]))
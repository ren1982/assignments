# Webscraper for heise.de - A University Assignment for Database Systems

This program was written as part of an assignment in the course Database Systems at the Freie Universität Berlin. The assignment was to create a Webscraper that takes all the headlines of articles in the category "https" on heise.de to determine the three most used words in all headlines.

---

## The Idea

Before programming the Webscraper, I had to first look at the actual website to see its structure and viewed its source code in order to find out the best way to grab the article titles. I noticed that all articles are listed inside a &lt;div> tag with the class name *keywordliste*. In addition, the actual titles are in a &lt;header>, which is also inside yet another &lt;div> tag. Finally, it was worth noting that the pages where the articles are listed are numbered in sequential order, with the first page having the number 0.

The assignment showed me a Webscraper at https://github.com/xconnect/fub.bsc.dbs.scraper.greyhound-data.com and from that I copied the `getPage()` function in order to connect to a page and create a BeautifulSoup object. Through the initial website videos I noted that all the pages I wanted to scrape had URLs which started with "https://www.heise.de/thema/https?seite=" which is why that was saved into a variable. allheaders and allwords, which collected all the headlines and all the words in the headlines, were also intitialized.

With help from a while loop all pages with articles can be accessed. The loop ends when a site does not have a &lt;div> tag with the class *keywordliste*. If the loop finds a valid URL, it finds all &lt;header> tags and saves its contents in the allheaders list. Once a headline is saved, regular expressions are used in order to extract the individual words and save them in the allwords list.

Once all headlines and words have been collected, the list of words is sorted, and how often each word is used is counted. All this is done with the help of the `unique()` function from Numerical Python (numpy). The generated tuples are then sorted in descending order based on counts, and the ten words/strings with the highest count are printed out.

## Challenges and Choices

1. Extracting words using regular expressions was somewhat tricky, as certain symbols such as apostrophes had to be included, while others such as colons had to be ignored.
2. Counting how often a word appears in the allwords list was originally coded with an explicit loop until I discovered and learned how to make it more efficient (or at least have less code) with the help of numpy and the `zip()` function.

## Code Credits

As mentioned earlier, `getPage()` was taken from the provided Greyhound Webscraper at https://github.com/xconnect/fub.bsc.dbs.scraper.greyhound-data.com .

Code on how to sort tuples was taken from https://stackoverflow.com/questions/14466068/sort-a-list-of-tuples-by-second-value-reverse-true-and-then-by-key-reverse-fal .
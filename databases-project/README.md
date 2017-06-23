# University Project for Database Systems

The contents of this folder are short programs I wrote for as part of a project requirement for the course Database Systems at the Freie Universität Berlin. The entire project can be found at https://git.imp.fu-berlin.de/rctx/dbs-projekt and was done together with two other Bachelor Computer Science students, Yannis Klingele and Rafael Taxis.

---

## The Project

The goal of the project is to create a visualisation of the most important tweets and hashtags by Hillary Clinton and Donald Trump from the 2016 US national election. A data set of more than 6000 tweets was provided to the students as both CSV and XLSX files. Our tasks included creating ER and Relational Models, creating the database, cleaning the data, importing the data into the database, and ultimately creating a metric for the comparison of hashtags used.

---

## The Files

There are two files included in this folder. **cleanexceldata.py** was created in order to clean the data provided and prepare it for importing, while **dataimport.py** was created in order to actually perform the import.

### cleanexceldata.py

#### The Idea

The data is already mostly clean (for example, no blank fields which shouldn't be empty, and all the given Twitter handles were correct), so the work done was minimal. The general idea:

1. The Excel Workbook containing our data is opened and two references are created, one to the Worksheet with the data, and one to a newly created Worksheet where we'll store our cleaned data.
2. We identify which columns will be used (for example, the Twitter handles and the tweets themselves) and leave out those that are unnecessary (for example, how or where the tweet was posted).
3. We iterate through every (useful) column systematically and copy each entry from the original Worksheet to the appropriate column in the new Worksheet.
4. Our group decided to store all timestamps into UNIX Time format, so I had to write code that takes a timestamp and converts it to the correct format before copying to the file. This code was  adapted from http://avilpage.com/2014/11/python-unix-timestamp-utc-and-their.html .
5. Once all the necessary values have been copied, the old Worksheet (with the original data set) is deleted, and the single Worksheet (with the cleaned data) is saved to a new Workbook; we don't want to overwrite the old Workbook in case something goes horribly wrong.

#### Challenges and Choices

1. Given the choice between working with the Excel Workbook and the CSV file, I decided to use the Excel Workbook because I was having issues with linebreaks/carriage returns within tweets in the CSV file. The parser was interpreting these carriage returns as new entries and not as part of the tweet, so there'd be more entries but with incomplete data. Working with the Excel Workbook meant that each tweet - including carriage returns - would be encased in its own cell, and thus there would be no issues with keeping tweets "contained" during the copy process (and ultimately the data import process).
2. I'm more familiar and comfortable with using Python as a programming language, which is why I decided on coding the program in Python.
3. Looking back, the timestamp conversion would have made sense as a separate function.

#### Code Credits

I needed a function that converted a row and column tuple into an Excel Cell Name and found that function at https://stackoverflow.com/questions/31420817/convert-excel-row-column-indices-to-alphanumeric-cell-reference-in-python-openpy .

As mentioned above, the UNIX Time converter was largely based on http://avilpage.com/2014/11/python-unix-timestamp-utc-and-their.html .

### dataimport.py

#### The Idea

The Python program takes our cleaned data, parses it, takes some additional information (such as parsing hashtags), and then imports it into our database. (We used a communal database provided for use by students of the university, and accordingly I have removed the particulars of this database such as hostname, username, and password from the code.)

Five functions were written to help with preparing our data for importing:

* `xlref(row, column)` is the same function we used in **cleanexceldata.py** to convert a row and column tuple to an Excel Cell Name.
* `tweetdata(rownumber)` reads an entire row from our Worksheet and returns a tuple with a tweet id (which we generated ourselves in order to uniquely identify each tweet), timestamp, author, retweet count, favourite count, and the actual text of the tweet (all of which can be found in our Excel file).
* `hashtaglist(tweet)` is the hashtag parser. It uses Regular Expressions to find hashtags within a tweet. The hashtags are then saved in various lists: A global list with all the hashtags from every tweet in our data set, a local list with all the hashtags from that particular tweet (including duplicates), another list of hashtags *without* duplicates, and finally a list of "new" hashtags discovered in the tweet (meaning these weren't in the global list before). The latter three lists are then returned.
* `zipidhashtag(tweet_id, hashtag_list)` takes a tweet and a list of its hashtags (including duplicates) and returns a list of tuples which includes the tweet id, a hashtag, and the number of times that hashtag appears in the tweet.
* `ziphashtags(hashtag_list)` takes a hashtag list (without duplicates) and returns the cross-product of all the hashtags in the list, excluding reflexive matches with itself.

The program works as follows:

1. We connect to our database and open our Excel Workbook to the Worksheet we want.
2. The program systematically goes through the Worksheet row by row (in other words, tweet by tweet) and runs the functions above in order to create tuples that can be imported into the database, into the respective tables (details of which I won't go into here).
3. Finally we commit the changes and close our database.

#### Challenges and Choices

1. It's rather inefficient to copy-paste `xlref(row, column)` into both programs instead of saving it (and other functions) into its own module to be imported, but ultimately this structure made it clearer to explain the functionality of both programs separately.
2. We made changes to our database models based on errors we encountered during the import process. Some were relatively trivial (such as naming our attribute names in lowercase), while some were slightly more complicated, such as discovering that there were a handful of hashtags that were used more than once in a single tweet, thus having to write a function that determines exactly that.
3. The biggest challenge was writing the hashtag parser because of the many rules of what constitutes a "valid" hashtag on Twitter. I was unable to find a(n official and) complete list of rules so I had to do a lot of trial-and-error on Twitter to see what is interpreted as a hashtag and what is not. For example, if several hashtags are written together without spaces between them, they won't be interpreted as hashtags. It took about two hours of additional testing and tweaking in order to get a "correct" hashtag parser.
4. There are certainly easier and more efficient ways to implement some of the functions above without explicitly using loops, but to be honest I learned about Python's built-in `map()` and `zip()` functions a little too late.
## English version of this README to follow!

Bevor wir einen Webscraper erstellen können, müssen wir erst herausfinden, wie die Webseite aufgebaut wird, was die Struktur ist, usw, um zu wissen, wonach unser Webscraper suchen soll. Darum haben wir die Webseite besucht und die Source-Datei (HTML Datei) angesehen. Wir merken, dass alle Artikeln zwischen den &lt;div> Tag mit der Klasse "keywordliste" aufgelistet werden. Zusätzlich finden wir jede Überschrift in (oder hinter) einem &lt;header> Tag, der sich auch in einem anderen &lt;div> Tag befindet. Zum Schluss merken wir, dass die Seiten sequentiell numeriert werden, wobei die erste Seite die 0. Seite ist.

Wir haben einfach die getPage Funktion aus dem Greyhound-Scraper kopiert und benutzt, damit wir ein BeautifulSoup Objekt erstellen können. Wir wissen, dass alle URLs mit "https://www.heise.de/thema/https?seite=" anfangen, deshalb haben wir dies in eine Variable gespeichert. Die Variablen allheaders und allwords werden auch initialisiert.

Eine while wird erzeugt, damit wir Zugriff auf alle Seiten mit Artikeln haben können. Die 0. Seite wird erst geöffnet, wird direkt zum &lt;div> Tag mit der Klasse "keywordliste" gegangen, und alle &lt;div> Tags darin werden gefunden. Nicht alle dieser &lt;div> Tags haben einen &lt;header> Tag, deswegen sollen wir überprüfen, ob den Wert von &lt;header> nicht None (also nicht leer) ist. Falls nicht, dann kriegen wir die Überschrift und fügen die in der allheaders Liste hinzu. Danach werden alle Wörter in jeder Überschrift mit Hilfe von Regular Expressions gefunden, und die werden in der allwords Liste gespeichert. Da wir später keine Probleme mit Vergleichungen haben wollen, werden alle Wörter klein geschrieben. Dieser Prozess wird für alle Seiten ausgeführt. Die Schleife terminiert, wenn die erste Seite gefunden wird, die keine &lt;div> Tag mit der Klasse "keywordliste" gefunden wird.

Danach werden alle Wörter sortiert und wird es gezählt, wie oft ein Wort auf der Liste vorkommt. Das entspricht, wie oft dieses Wort in einer Überschrift vorkommt. Am Ende haben wir eine Liste von Tupeln mit dem Wort und der Anzahl. Dies werden wieder sortiert, und die Top 10 Wörter (oder Strings, da einige gefundene Strings keine Wörter der deutschen Sprache sind) werden zurückgegeben. Laut Duden ist "https" kein deutsches Wort (also es gibt keine Definition in Duden für "https", Quelle: http://www.duden.de/suchen/shop/https), deswegen sind unsere Top 3 Deutsche Wörter:

1. und (36)
2. für (32)
3. mit (28)

Hochgeladen sind zwei Varianten. **heisescraper.py** zählt alle Vorkommen eines Worts durch eine explizite Schleife, wobei **heisescrapernp.py** nutzt die unique Funktion des Moduls numpy (Numerical Python), um diese Operation zu machen.
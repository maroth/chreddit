import time
import sqlite3 as sqlite
import praw
import feedparser
import random

feeds = [
    'http://www.20min.ch/rss/rss.tmpl?type=rubrik&get=3', #20min international 
    'http://www.20min.ch/rss/rss.tmpl?type=rubrik&get=2', #20min schweiz
    'http://www.20min.ch/rss/rss.tmpl?type=channel&get=8', #20min wirtschaft und boerse
    'http://www.20min.ch/rss/rss.tmpl?type=channel&get=4', #20min news
    'http://www.20min.ch/rss/rss.tmpl?type=channel&get=1', #20min frontpage
    'http://www.nzz.ch/aktuell/international.rss', #nzz international
    'http://www.nzz.ch/aktuell/wirtschaft/uebersicht.rss', #nzz wirtschaft
    'http://www.nzz.ch/aktuell/schweiz.rss', #nzz schweiz
    'http://www.nzz.ch/wissen/uebersicht.rss', #nzz wissenschaft
    'http://www.tagesanzeiger.ch/rss.html', #tagesanzeiger front
    'http://www.tagesanzeiger.ch/schweiz/rss.html', #tagesanzeiger schweiz
    'http://www.tagesanzeiger.ch/ausland/rss.html', #tagesanzeiger ausland
    'http://www.tagesanzeiger.ch/wirtschaft/rss.html', #tagesanzeiger wirtschaft
    #'http://weltwoche.ch/rss/online-exklusiv.html', #weltwoche online-exlusiv
]

con = None

connection = sqlite.connect('submission_db')
try:
    connection.execute('CREATE TABLE submissions(submission TEXT)')
    connection.commit()
except sqlite.OperationalError:
    pass

reddit = praw.Reddit(user_agent='chreddit 1.0')
reddit.login('transpostmeta', 'styles', disable_warning=True)

def is_submitted(link):
    cursor = connection.cursor()
    query = 'SELECT COUNT(*) FROM submissions WHERE submission = "' + entry.link + '"'
    cursor.execute(query)
    data = cursor.fetchone()
    connection.commit()
    return data[0] == 1

def post(title, link):
   connection.execute('INSERT INTO submissions VALUES ("' + entry.link + '")')
   connection.commit()
   title = entry.title
   reddit.submit('schweizermedien', title, url=link)

while True:
    feed_address = random.choice(feeds)
    feed = feedparser.parse(feed_address)
    for entry in feed.entries:
        if not is_submitted(entry.link):
            print 'posting: ' + entry.title
            post(entry.title, entry.link)
            time.sleep(5)
            break
                


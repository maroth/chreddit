import time
import HTMLParser
import sqlite3 as sqlite
import praw
import feedparser
import random

feeds = [
    #SCHWEIZ
    'http://www.20min.ch/rss/rss.tmpl?type=rubrik&get=2', #20min schweiz
    'http://www.blick.ch/news/schweiz/rss.xml', #Blick Schweiz
    'http://www.nzz.ch/aktuell/schweiz.rss', #nzz schweiz
    'http://www.tagesanzeiger.ch/schweiz/rss.html', #tagesanzeiger schweiz
    'http://www.srf.ch/news/bnf/rss/1890', #srf schweiz
    'http://www.derbund.ch/schweiz/rss.html', #Der Bund Schweiz
    'http://www.bernerzeitung.ch/schweiz/rss.html', #Berner Zeitung Schweiz
    'http://bazonline.ch/schweiz/rss.html', #Basler Zeitung Schweiz
    'http://www.tagblatt.ch/storage/rss/rss/nachrichten-politik-schweiz.xml', #St. Galler Tagblatt Schweiz

    #BERN
    'http://www.derbund.ch/bern/rss.html', #Der Bund Bern
    'http://www.bernerzeitung.ch/region/bern/rss.html', #Berner Zeitung Bern

    #BASEL
    'http://bazonline.ch/basel/rss.html', #Basler Zeitung Basel

    #ZÜRICH
    'http://www.nzz.ch/zuerich.rss', #nzz Zuerich
    'http://www.tagesanzeiger.ch/zuerich/rss.html', #tagesanzeiger Zuerich

    #ST. GALLEN
    'http://www.tagblatt.ch/storage/rss/rss/ostschweiz-stgallen-stadt-stgallen.xml', #St. Galler Tagblatt Stadt St. Gallen

    #ZENTRALSCHWEIZ
    'http://www.luzernerzeitung.ch/storage/rss/rss/zentralschweiz.xml', #Luzerner Zeitung (Neues aus der Zentralschweiz)


    #'http://www.20min.ch/rss/rss.tmpl?type=rubrik&get=3', #20min international 
    #'http://www.20min.ch/rss/rss.tmpl?type=channel&get=8', #20min wirtschaft und boerse
    #'http://www.20min.ch/rss/rss.tmpl?type=channel&get=4', #20min news
    #'http://www.20min.ch/rss/rss.tmpl?type=channel&get=1', #20min frontpage
    #'http://www.nzz.ch/aktuell/international.rss', #nzz international
    #'http://www.nzz.ch/aktuell/wirtschaft/uebersicht.rss', #nzz wirtschaft
    #'http://www.nzz.ch/wissen/uebersicht.rss', #nzz wissenschaft
    #'http://www.tagesanzeiger.ch/rss.html', #tagesanzeiger front
    #'http://www.tagesanzeiger.ch/ausland/rss.html', #tagesanzeiger ausland
    #'http://www.tagesanzeiger.ch/wirtschaft/rss.html', #tagesanzeiger wirtschaft
    #'http://weltwoche.ch/rss/online-exklusiv.html', #weltwoche online-exlusiv
    #'http://www.srf.ch/news/bnf/rss/1922', #srf international
    #'http://www.srf.ch/news/bnf/rss/1926', #srf wirtschaft
    #'http://www.srf.ch/news/bnf/rss/1930', #arf panorama
    #'http://www.srf.ch/wissen/bnf/rss/8354', #srf technik
    #'http://www.srf.ch/wissen/bnf/rss/8314', #srf digital
    #'http://www.srf.ch/wissen/bnf/rss/8326', #srf mensch
    #'http://www.srf.ch/wissen/bnf/rss/8338', #srf natur
    #'http://www.derbund.ch/rss.html', #Der Bund Front
    #'http://www.derbund.ch/ausland/rss.html', #Der Bund Ausland
    #'http://www.derbund.ch/wirtschaft/rss.html', #Der Bund Wirschaft
    #'http://www.derbund.ch/digital/rss.html', #Der Bund Digital 
    #'http://bazonline.ch/rss.html', #Basler Zeitung 
    #'http://bazonline.ch/ausland/rss.html', #Basler Zeitung Ausland 
    #'http://bazonline.ch/wirtschaft/rss.html', #Basler Zeitung Schweiz
    #'http://bazonline.ch/digital/rss.html', #Basler Zeitung Digital
    #'http://www.blick.ch/news/rss.xml', #Blick News
    #'http://www.blick.ch/news/ausland/rss.xml', #Blick Ausland
    #'http://www.blick.ch/news/wirtschaft/rss.xml', #Blick Wirtschaft
    #'http://www.blick.ch/news/wissenschaftundtechnik/rss.xml', #Blick Wissen
    #'http://www.tagblatt.ch/storage/rss/rss/nachrichten-politik-international.xml', #St. Galler Tagblatt International
    #'http://www.tagblatt.ch/storage/rss/rss/nachrichten-wirtschaft.xml', #St. Galler Tagblatt Wirtschaft
]

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

def make_submission_title(title, description):
    max_length = 300
    suffix = '...'
    htmlParser = HTMLParser.HTMLParser()
    submission_title = htmlParser.unescape(entry.title)
    if entry.description:
        description = htmlParser.unescape(entry.description)
        submission_title += ' ' + u'\u2014' + ' ' + description
    if len(submission_title) <= 300:
        return submission_title
    else:
        submission_title = submission_title[:max_length + 1 - len(suffix)]
        submission_title = ' '.join(submission_title.split(' ')[0:-1]) + suffix
        return submission_title

def post(title, link):
    connection.execute('INSERT INTO submissions VALUES ("' + entry.link + '")')
    connection.commit()
    title = make_submission_title(entry.title, entry.description)
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
                


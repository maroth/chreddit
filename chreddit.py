import sql 
import time
import HTMLParser
import praw
import feedparser
import random
import feeds

reddit = praw.Reddit(user_agent='chreddit 1.0')
username = os.environ['REDDIT_USERNAME']
password = os.environ['REDDIT_PASSWORD']
reddit.login(username, password, disable_warning=True)

feed_address = random.choice(feeds.feeds)
feed = feedparser.parse(feed_address)
for entry in feed.entries:
	if not sql.exists(entry.link):
		post(entry.title, entry.link)

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
	sql.submit(entry.title)
    title = make_submission_title(entry.title, entry.description)
    reddit.submit('schweizermedien', title, url=link)


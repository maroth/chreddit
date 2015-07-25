import sql, time, os, HTMLParser, praw, feedparser, random, feeds, logging
from apscheduler.schedulers.blocking import BlockingScheduler

logging.basicConfig()
scheduler = BlockingScheduler()

reddit = praw.Reddit(user_agent='chreddit 1.0')
username = os.environ['REDDIT_USERNAME']
password = os.environ['REDDIT_PASSWORD']
reddit.login(username, password, disable_warning=True)

@scheduler.scheduled_job('interval', seconds=1)
def select_article():
    feed_address = random.choice(feeds.feeds)
    feed = feedparser.parse(feed_address)
    for entry in feed.entries:
        if not sql.submitted(entry.link) and not sql.submitted(entry.title):
            post(entry)
            break

def post(entry):
    sql.submit(entry.link)
    sql.submit(entry.title)
    title = make_submission_title(entry.title, entry.description)
    subreddit = os.environ['SUBREDDIT']
    reddit.submit(subreddit, title, url=entry.link)
    
def make_submission_title(title, description):
    max_length = 300
    suffix = '...'
    htmlParser = HTMLParser.HTMLParser()
    submission_title = htmlParser.unescape(title)
    if description:
        description = htmlParser.unescape(description)
        submission_title += ' ' + u'\u2014' + ' ' + description
    if len(submission_title) <= 300:
        return submission_title
    else:
        submission_title = submission_title[:max_length + 1 - len(suffix)]
        submission_title = ' '.join(submission_title.split(' ')[0:-1]) + suffix
        return submission_title


scheduler.start()

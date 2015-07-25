import sql, time, os, HTMLParser, praw, feedparser, random, feeds, logging
from apscheduler.schedulers.blocking import BlockingScheduler

logging.basicConfig()
scheduler = BlockingScheduler()


@scheduler.scheduled_job('interval', seconds=1)
def post_news_to_reddit():
    reddit = praw.Reddit(user_agent='chreddit 1.0')
    username = os.environ['REDDIT_USERNAME']
    password = os.environ['REDDIT_PASSWORD']
    reddit.login(username, password, disable_warning=True)

    feed_address = random.choice(feeds.feeds)
    feed = feedparser.parse(feed_address)
    for entry in feed.entries:
        if not sql.submitted(entry.link):
            post(entry)

def post(entry):
    sql.submit(entry.title)
    title = make_submission_title(entry.title, entry.description)
    subreddit = es.environ['SUBREDDIT']
    reddit.submit(subreddit, title, url=entry.link)
    
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


scheduler.start()

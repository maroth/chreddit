import sql, feeds, config
import feedparser, HTMLParser, praw
import random

reddit = praw.Reddit(user_agent=config.user_agent)
reddit.login(config.username, config.password, disable_warning=True)

def submit_article():
    feed_address = random.choice(feeds.feeds)
    feed = feedparser.parse(feed_address)
    for entry in reversed(feed.entries):
        if not sql.submitted(entry.link) and not sql.submitted(entry.title):
            post(entry)
            break

def post(entry):
    title = make_submission_title(entry.title, entry.description)
    print ('submitting: ' + title).encode('utf-8')
    sql.submit(entry.link)
    sql.submit(entry.title)
    reddit.submit(config.subreddit, title, url=entry.link)
    
def make_submission_title(title, description):
    htmlParser = HTMLParser.HTMLParser()
    submission_title = htmlParser.unescape(title)
    if description:
        description = htmlParser.unescape(description)
        submission_title += ' ' + config.separator + ' ' + description
    if len(submission_title) <= config.max_length:
        return submission_title
    else:
        #cut the title to the max length minus the suffix length...
        submission_title = submission_title[:config.max_length + 1 - len(config.suffix)]
        #then remove the last word (as it might be incomplete) and append the suffix
        submission_title = ' '.join(submission_title.split(' ')[0:-1]) + config.suffix
        return submission_title

for _ in range(config.submissions_per_run):
    submit_article();

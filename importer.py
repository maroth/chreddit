from dataAccess import DataAccess
import feeds, config
import feedparser, HTMLParser

from models import Submission

class Importer:
    dataAccess = DataAccess()
    parse_feed = feedparser.parse

    def importFeed(self, feeds):
        for feed_address in feeds:
            feed = self.parse_feed(feed_address)
            for entry in feed.entries:
                self.process(entry, feed_address)

    def process(self, entry, feed):
        if not self.dataAccess.exists(entry.link):
            submission = Submission(title=entry.title, description=entry.description, url=entry.link, feed=feed)
            self.dataAccess.save(submission)

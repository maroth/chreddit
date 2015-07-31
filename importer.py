from dataAccess import DataAccess
from feedparser import parse

from models import Submission


class Importer:
    dataAccess = DataAccess()

    def parse_feed(self, feed_address):
        return parse(feed_address)

    def import_feeds(self, feed_addresses):
        for feed_address in feed_addresses:
            print 'checking feed: ' + feed_address
            feed = self.parse_feed(feed_address)
            for entry in feed.entries:
                self.process(entry, feed_address)

    def process(self, entry, feed):
        if not self.dataAccess.exists(entry.link):
            print 'saving new feed entry: ' + entry.link
            submission = Submission(
                title=entry.title,
                description=entry.description,
                url=entry.link,
                feed=feed)
            self.dataAccess.save(submission)

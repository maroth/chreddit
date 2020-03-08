from dataAccess import DataAccess
from feedparser import parse
import traceback

from models import Submission


class Importer:
    dataAccess = DataAccess()

    def parse_feed(self, feed_address):
        return parse(feed_address[0])

    def import_feeds(self, feed_addresses):
        for feed_address in feed_addresses:
            print ('checking feed: ' + str(feed_address))
            feed = self.parse_feed(feed_address)
            for entry in feed.entries:
                self.process(entry, feed_address)

    def process(self, entry, feed):
        if not self.dataAccess.exists(entry.link):
            print ('saving new feed entry: ' + entry.link)
            try:
                submission = Submission(
                    title=entry.title,
                    description=entry.description\
                        if hasattr(entry, 'description') else '',
                    url=entry.link,
                    feed_url=feed[0],
                    feed_name=feed[1])
                self.dataAccess.save(submission)
            except:
                traceback.print_exc()


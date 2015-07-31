#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from mock import MagicMock, Mock, call

from models import Submission, Base
from importer import Importer
from utils import Expando


class TestImporter:
    def setup(self):
        self.engine = create_engine('sqlite://')
        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)
        Base.metadata.create_all(self.engine)

        self.importer = Importer()
        self.importer.dataAccess.Session = self.Session

        self.entry1 = Expando()
        self.entry1.title = u'entry 1 title é'
        self.entry1.description = u'entry 1 description é'
        self.entry1.link = u'http://entry1.linké'

        self.entry2 = Expando()
        self.entry2.title = u'entry 2 title é'
        self.entry2.description = u'entry 2 description é'
        self.entry2.link = self.entry1.link

        self.entry3 = Expando()
        self.entry3.title = u'entry 3 title é'
        self.entry3.description = u'entry 3 description é'
        self.entry3.link = u'http://entry3.linké'

        self.entry4 = Expando()
        self.entry4.title = u'entry 4 title é'
        self.entry4.description = u'entry 4 description é'
        self.entry4.link = u'http://entry4.linké'

        self.entry5 = Expando()
        self.entry5.title = u'entry 4 title é'
        self.entry5.link = u'http://entry4.linké'

        self.feed1 = u'http://feed1url.urlé'
        self.feed2 = u'http://feed2url.urlé'

        self.feed1contents = Expando()
        self.feed1contents.entries = [self.entry1, self.entry2]
        self.feed2contents = Expando()
        self.feed2contents.entries = [self.entry3, self.entry4]

    def teardown(self):
        Base.metadata.drop_all(self.engine)

    def test_process_newSubmission_isSaved(self):
        self.importer.process(self.entry1, self.feed1)

        saved = self.Session().query(Submission).first()
        assert saved.title == self.entry1.title
        assert saved.description == self.entry1.description
        assert saved.url == self.entry1.link
        assert saved.feed == self.feed1
        assert saved.created != None

    def test_process_submissionWithExistingLink_isNotSaved(self):
        self.importer.process(self.entry1, self.feed1)
        self.importer.process(self.entry2, self.feed2)

        assert self.Session().query(Submission).count() == 1

    def test_process_submissionWithNoDescription_isSaved(self):
        self.importer.process(self.entry5, self.feed1)

        assert self.Session().query(Submission).count() == 1

    def test_importFeeds_entriesAreSaved(self):
        self.importer.parse_feed = Mock(
            side_effect=[self.feed1contents, self.feed2contents])
        self.importer.process = MagicMock()

        self.importer.import_feeds([self.feed1, self.feed2])

        self.importer.process.assert_has_calls(
            [call(self.entry1, self.feed1),
             call(self.entry2, self.feed1),
             call(self.entry3, self.feed2),
             call(self.entry4, self.feed2)])

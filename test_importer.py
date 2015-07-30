#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import exists

from models import Submission, Base
import config
from importer import Importer

import dataAccess

class Expando(object):
    pass

class TestImporter:
    def setup(self):
        self.engine = create_engine('sqlite://')
        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)
        Base.metadata.create_all(self.engine)

        self.importer = Importer()
        self.importer.dataAccess.Session = self.Session

    def teardown(self):
        Base.metadata.drop_all(self.engine)

    def test_newSubmission_isSaved(self):
        entry = Expando()
        entry.title = u'My Tést Tïtle'
        entry.description = u'A really long description that is really long'
        entry.link = u'http://www.20min.ch/some/link/to?=rg43'
        feed = u'http://www.20min.ch/rss/rss.tmpl?type=rubrik&get=2'

        self.importer.process(entry, feed)

        saved = self.Session().query(Submission).first()
        assert saved.title == entry.title
        assert saved.description == entry.description
        assert saved.url == entry.link
        assert saved.feed == feed
        
    def test_submissionWithExistingLink_isNotSaved(self):
        entry1 = Expando()
        entry1.title = u'My Tést Tïtle'
        entry1.description = u'A really long description that is really long'
        entry1.link = u'http://www.20min.ch/some/link/to?=rg43'
        feed1 = u'http://www.20min.ch/rss/rss.tmpl?type=rubrik&get=2'

        entry2 = Expando()
        entry2.title = u'é'
        entry2.description = u'é'
        entry2.link = entry1.link
        feed2 = u'f7uy34ré'

        self.importer.process(entry1, feed1)
        self.importer.process(entry2, feed2)

        assert self.Session().query(Submission).count() == 1




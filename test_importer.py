#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import exists 

from models import Submission
import config
from importer import Importer

Base = declarative_base()
import dataAccess

class Expando(object):
    pass

class TestImporter:
    def test_save(self):
        engine = create_engine('sqlite://')
        Session = sessionmaker()
        Session.configure(bind=engine)
        Base.metadata.create_all(engine)

        entry = Expando()
        entry.title = 'My Tést Tïtle'
        entry.description = 'A really long description that is really long'
        entry.link = 'http://www.20min.ch/some/link/to?=rg43'
        feed = 'http://www.20min.ch/rss/rss.tmpl?type=rubrik&get=2'

        importer = Importer()
        importer.dataAccess.Session = Session

        importer.process(entry, feed)

        assert Session().query(exists().where(Submission.url==url)).scalar()
        




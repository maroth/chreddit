#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import datetime

import config

Base = declarative_base()


class Submission(Base):
    __tablename__ = config.tablename

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    url = Column(String)
    feed_name = Column(String)
    feed_url = Column(String)
    created = Column(DateTime, default=datetime.datetime.now())
    submitted = Column(DateTime)
    submission_id = Column(String)
    duplicate_of = Column(Integer, ForeignKey(config.tablename + '.id'))

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import config
from models import Submission
from sqlalchemy import desc, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists


class DataAccess:
    engine = create_engine(config.database_url)
    Session = sessionmaker()
    Session.configure(bind=engine)

    def save(self, submission):
        session = self.Session()
        session.add(submission)
        session.commit()
        self.rollingDelete()

    def rollingDelete(self):
        # free database in heroku has limited rows,
        # so delete old ones in a rolling fashion
        session = self.Session()
        to_delete = session.query(Submission.id)\
            .order_by(desc(Submission.created))\
            .offset(config.max_rows).all()
        session.commit()
        to_delete_ids = [i[0] for i in to_delete]
        if to_delete_ids:
            print 'deleting '\
                + str(len(to_delete_ids))\
                + ' items from database'
            session.query(Submission)\
                .filter(Submission.id.in_(to_delete_ids))\
                .delete(synchronize_session='fetch')
            session.commit()
        session.close()

    def submit(self, submission):
        session = self.Session()
        session.query(Submission)\
            .filter(Submission.id == submission.id)\
            .update({
                Submission.submitted: datetime.datetime.now()
            })

    def exists(self, url):
        session = self.Session()
        result = session.query(exists().where(Submission.url == url)).scalar()
        session.close()
        return result

    def all_unsubmitted(self):
        session = self.Session()
        result = session.query(Submission)\
            .filter(Submission.submitted == None)
        session.close()
        return result

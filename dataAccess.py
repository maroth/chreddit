#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import config
from models import Submission, Base
from sqlalchemy import desc, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists


class DataAccess:
    def __init__(self):
        engine = create_engine(config.database_url)
        self.Session = sessionmaker()
        self.Session.configure(bind=engine)
        Base.metadata.create_all(engine)


    def save(self, submission):
        session = self.Session()
        session.add(submission)
        session.commit()
        #self.rollingDelete()


    def all_unsubmitted(self):
        session = self.Session()
        result = session.query(Submission).filter(Submission.submitted == None).all()
        session.close()
        return result


    def find_oldest_submitted_duplicate(self, submission):
        session = self.Session()
        result = session.query(Submission)\
            .filter(Submission.title == submission.title)\
            .filter(Submission.url != submission.url)\
            .filter(Submission.submission_id != None)\
            .filter(Submission.submitted != None)\
            .order_by(desc(Submission.submitted))\
            .first()
        session.close()
        return result


    def submit(self, submission, submitted):
        session = self.Session()
        session.query(Submission)\
            .filter(Submission.id == submission.id)\
            .update({
                Submission.submitted: datetime.datetime.now(),
            })
        if submitted is not None:
            session.query(Submission)\
                .filter(Submission.id == submission.id)\
                .update({
                    Submission.submission_id: submitted.id,
                })
        session.commit()
        session.close()
        
        
    def submit_duplicate(self, submission, duplicate, reply):
        session = self.Session()
        
        session.query(Submission)\
            .filter(Submission.id == submission.id)\
            .update({
                Submission.submitted: datetime.datetime.now(),
                Submission.duplicate_of: duplicate.id,
                Submission.submission_id: reply.id
            })

        session.commit()
        session.close()

    def exists(self, url):
        session = self.Session()
        result = session.query(exists().where(Submission.url == url)).scalar()
        session.close()
        return result


    def all(self):
        session = self.Session()
        result = session.query(Submission)
        session.close()
        return result


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
            print ('deleting '\
                + str(len(to_delete_ids))\
                + ' items from database')
            session.query(Submission)\
                .filter(Submission.id.in_(to_delete_ids))\
                .delete(synchronize_session='fetch')
            session.commit()
        session.close()

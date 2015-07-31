#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from mock import Mock, call

from submitter import Submitter
from models import Submission, Base
from utils import Expando, create_submission

class TestSubmitter:
    def setup(self):
        self.engine = create_engine('sqlite://')
        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)
        Base.metadata.create_all(self.engine)

        self.submitter = Submitter()
        self.submitter.dataAccess.Session = self.Session

        self.submitter.reddit = Mock()

    def teardown(self):
        Base.metadata.drop_all(self.engine)

    def test_submitAllUnsubmitted_unsubmittedSubmission_isSubmitted(self):
        unsubmitted = create_submission(submitted=None)
        self.submitter.dataAccess.save(unsubmitted)

        self.submitter.submit_all_unsubmitted()

        assert self.submitter.reddit.submit.called

        

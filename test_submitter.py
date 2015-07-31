#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from mock import Mock

from submitter import Submitter
from models import Base
from utils import create_submission
import config


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

    def test_submitAllUnsubmitted_submittedSubmission_isNotSubmitted(self):
        submitted = create_submission()
        self.submitter.dataAccess.save(submitted)

        self.submitter.submit_all_unsubmitted()

        assert not self.submitter.reddit.submit.called

    def test_makeSubmissionTitle_shortValues_concatenatesCorrectly(self):
        title = self.submitter.make_submission_title(
            'title', 'description', 100)
        assert title == 'title ' + config.separator + ' description'

    def test_makeSubmissionTitle_longValues_cutsCorrectly(self):
        title = self.submitter.make_submission_title(
            'hans', 'guck in die luft', 12 + len(config.suffix))
        assert title == 'hans ' + config.separator + ' guck' + config.suffix

        title = self.submitter.make_submission_title(
            'hans', 'guck in die luft', 14 + len(config.suffix))
        assert title == 'hans ' + config.separator + ' guck in' + config.suffix

    def test_makeSubmissionTitle_noDescription_noSuffix(self):
        title = self.submitter.make_submission_title('hans', '', 100)
        assert title == 'hans'

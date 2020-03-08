#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from mock import Mock

from submitter import Submitter
from models import Base
from utils import create_submission
import config
import unittest


class SubmitterTestCase(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite://')
        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)
        Base.metadata.create_all(self.engine)

        self.submitter = Submitter()
        self.submitter.dataAccess.Session = self.Session

        self.submitter.reddit = Mock()

    def tearDown(self):
        Base.metadata.drop_all(self.engine)


class Submit_UnsubmittedSubmission_SubmitCalled_TestCase(SubmitterTestCase):
    def runTest(self):
        # Arrange
        unsubmitted = create_submission(submitted=None)
        submit_response = Mock()
        submit_response.id(return_value=12)
        self.submitter.reddit.submit(return_value=submit_response)
        self.submitter.dataAccess.save(unsubmitted)

        # Act
        self.submitter.submit_all_unsubmitted()

        # Assert
        self.assertTrue(self.submitter.reddit.submit.called)


class SubmitAllUnsubmitted_NoUnsubmittedSubmission_SubmitNotCalled_TestCase(SubmitterTestCase):
    def runTest(self):
        # Arrange
        submitted = create_submission()
        self.submitter.dataAccess.save(submitted)

        # Act
        self.submitter.submit_all_unsubmitted()

        # Assert
        self.assertFalse(self.submitter.reddit.submit.called)


class MakeSubmissionTitle_ShortString_ConcatenatesTitleAndDescription_TestCase(SubmitterTestCase):
    def runTest(self):
        # Act
        title = self.submitter.make_submission_title('title', 'description', 100)

        # Assert
        self.assertEqual('title ' + config.separator + ' description', title)


class MakeSubmissionTitle_TooLongString_ShortensToBelowMaxValue_TestCase(SubmitterTestCase):
    def runTest(self):
        # Act
        title = self.submitter.make_submission_title('hans', 'guck in die luft', 12 + len(config.suffix))

        # Assert
        self.assertEqual('hans ' + config.separator + ' guck' + config.suffix, title)


class MakeSubmissionTitle_TooLongString_ShortensToBelowMaxValue_TestCase(SubmitterTestCase):
    def runTest(self):
        # Act
        title = self.submitter.make_submission_title('hans', 'guck in die luft', 14 + len(config.suffix))

        # Assert
        self.assertEqual('hans ' + config.separator + ' guck in' + config.suffix, title)


class MakeSubmissionTitle_NoDescription_NoSuffixAppended_TestCase(SubmitterTestCase):
    def runTest(self):
        # Arrange
        title = self.submitter.make_submission_title('hans', '', 100)

        # Act

        # Assert
        self.assertEqual('hans', title)


if __name__ == '__main__':
        unittest.main()

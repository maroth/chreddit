#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.sql import exists
from sqlalchemy.orm import sessionmaker
from mock import Mock, ANY
from models import Submission

from submitter import Submitter
from models import Base
from utils import create_submission
import config
import unittest


class SubmitterTestCase(unittest.TestCase):
    def setUp(self):
        config.database_url = 'sqlite://'
        self.engine = create_engine('sqlite://')
        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)
        Base.metadata.create_all(self.engine)

        self.submitter = Submitter()
        self.submitter.dataAccess.Session = self.Session

        self.submitter.reddit = Mock()

        self.subreddit = Mock()
        self.submitter.reddit.subreddit.return_value = self.subreddit

    def tearDown(self):
        Base.metadata.drop_all(self.engine)


    def getSubmission(self, id):
        session = self.Session()
        return session.query(Submission).filter(Submission.id == id).first()


    def persistSubmission(self, submission):
        session = self.Session()
        session.add(submission)
        session.commit()


class Submit_UnsubmittedSubmission_Submitted_TestCase(SubmitterTestCase):
    def runTest(self):
        # Arrange
        unsubmitted = create_submission(submitted=None)
        self.persistSubmission(unsubmitted)
        id = unsubmitted.id

        submission_id = "123a"
        self.subreddit.submit.return_value = Mock(id=submission_id)

        # Act
        self.submitter.submit_all_unsubmitted()

        # Assert
        self.submitter.reddit.subreddit.assert_called_with(config.subreddit)
        self.subreddit.submit.assert_called_with(ANY, url=unsubmitted.url)
        self.assertFalse(self.getSubmission(id).submitted == None)
        self.assertEquals(submission_id, self.getSubmission(id).submission_id)


class SubmitAllUnsubmitted_NoUnsubmittedSubmission_SubmitNotCalled_TestCase(SubmitterTestCase):
    def runTest(self):
        # Arrange
        submitted = create_submission()
        self.persistSubmission(submitted)
        dt_submitted = submitted.submitted
        id = submitted.id

        # Act
        self.submitter.submit_all_unsubmitted()

        # Assert
        self.submitter.reddit.subreddit.assert_not_called()
        self.assertEqual(dt_submitted, self.getSubmission(id).submitted)


class Submit_UnsubmittedSubmissionWithTitleEqualToSubmittedSubmission_CommentPosted_TestCase(SubmitterTestCase):
    def runTest(self):
        # Arrange
        original = create_submission(url="url1")
        duplicate = create_submission(submitted=None, url="url2")
        self.persistSubmission(original)
        self.persistSubmission(duplicate)
        original_id = original.id
        duplicate_id = duplicate.id
        comment_id = "13ds"

        original_submission_id = original.submission_id
        original_post = Mock(id=original_submission_id)
        original_post.reply.return_value = Mock(id=comment_id)
        self.submitter.reddit.submission.return_value = original_post

        # Act
        self.submitter.submit_all_unsubmitted()

        # Assert
        self.submitter.reddit.submission.assert_called_with(id=original_submission_id)
        original_post.reply.assert_called_with(ANY)

        self.assertFalse(self.getSubmission(duplicate_id).submitted == None)
        self.assertEqual(self.getSubmission(duplicate_id).duplicate_of, original_id)
        self.assertEqual(self.getSubmission(duplicate_id).submission_id, comment_id)


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

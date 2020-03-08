#!/usr/bin/env python
# -*- coding: utf-8 -*-

import praw
from html.parser import HTMLParser
import traceback
from random import shuffle

from dataAccess import DataAccess
import config
import feeds
import time
import re


class Submitter:
    dataAccess = DataAccess()
    reddit = praw.Reddit(client_id=config.client_id, client_secret=config.client_secret, user_agent=config.user_agent, redirect_uri='http://localhost:8080', username=config.username, password=config.password)

    def submit_all_unsubmitted(self):
        submissions = self.dataAccess.all_unsubmitted()
        shuffle(submissions)
        for submission in submissions:
            self.submit(submission)
            time.sleep(0.5)

    def submit(self, submission):
        post_with_same_title = self.dataAccess.submitted_with_title(submission.title)
        if post_with_same_title is not None:
            self.post_already_submitted_comment(post_with_same_title, submission)
        else:
            self.post_submission(submission)

    def post_submission(self, submission):
        title = self.make_submission_title(
            submission.title,
            submission.description,
            config.max_length)
        try:
            print('submitting: ' + title)
            try:
                submitted = self.reddit.subreddit(config.subreddit).submit(title, url=submission.url)
            except Exception as ex:
                print(ex)
                submitted = None
            self.dataAccess.submit(submission, submitted)
        except:
            print('error submitting')
            traceback.print_exc()


    def post_already_submitted_comment(self, post_with_same_title, submission):
        try:
            existing_submission = self.reddit.submission(id=post_with_same_title.submission_id)
        except:
            print('error getting already submitted post')
            return

         #markdown for links is [link title](http://link.com)
        comment_text = '[{}{}]({})'.format(
            config.other_source_prefix,
            submission.feed_name,
            submission.url)
        try:
            print('commenting: ' + comment_text)
            reply = existing_submission.reply(comment_text)
        except:
            print('error commenting')
            reply = None
            traceback.print_exc()

        self.dataAccess.submit_duplicate(submission, post_with_same_title, reply)


    def make_submission_title(self, title, description, max_length):
        submission_title = title
        if description != '':
            submission_title += ' ' + config.separator + ' ' + description

        htmlParser = HTMLParser()

        # remove html-encoded special characters 
        submission_title = htmlParser.unescape(submission_title)

        # remove all closed html tags within the tigle (e.g. images)
        submission_title = re.sub('<[^<]+?>', '', submission_title)

        # remove multiple whitespaces
        submission_title = ' '.join(submission_title.split())

        if len(submission_title) <= max_length:
            return submission_title
        else:
            # cut the title to the max length minus the suffix length...
            submission_title =\
                submission_title[:max_length + 1 - len(config.suffix)]
            # then remove the last word (as it might be incomplete)
            # and append the suffix
            submission_title =\
                ' '.join(submission_title.split(' ')[0:-1]) + config.suffix
            return submission_title

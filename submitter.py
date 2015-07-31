#!/usr/bin/env python
# -*- coding: utf-8 -*-
import praw
import sys
import HTMLParser

from dataAccess import DataAccess
import config


class Submitter:
    dataAccess = DataAccess()
    reddit = praw.Reddit(user_agent=config.user_agent)

    def login(self):
        reddit.login(config.username, config.password, disable_warning=True)

    def submit_all_unsubmitted(self):
        submissions = self.dataAccess.all_unsubmitted()
        for submission in submissions:
            try:
                self.post(submission)
            except:
                print 'error submitting'

    def post(self, submission):
        title = self.make_submission_title(submission.title, submission.description)
        print ('submitting: ' + title).encode('utf-8')
        self.reddit.submit(config.subreddit, title, url=submission.url)
        self.dataAccess.submit(submission)

    def make_submission_title(self, title, description):
        htmlParser = HTMLParser.HTMLParser()
        submission_title = htmlParser.unescape(title)
        if description:
            description = htmlParser.unescape(description)
            submission_title += ' ' + config.separator + ' ' + description
        if len(submission_title) <= config.max_length:
            return submission_title
        else:
            #cut the title to the max length minus the suffix length...
            submission_title = submission_title[:config.max_length + 1 - len(config.suffix)]
            #then remove the last word (as it might be incomplete) and append the suffix
            submission_title = ' '.join(submission_title.split(' ')[0:-1]) + config.suffix
            return submission_title

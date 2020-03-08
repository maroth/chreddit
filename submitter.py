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
    def __init__(self):
        self.dataAccess = DataAccess()
        self.reddit = praw.Reddit(
                client_id=config.client_id, 
                client_secret=config.client_secret, 
                user_agent=config.user_agent, 
                redirect_uri='http://localhost:8080', 
                username=config.username, 
                password=config.password)


    def submit_all_unsubmitted(self):
        submissions = self.dataAccess.all_unsubmitted()
        shuffle(submissions)
        for submission in submissions:
            self.submit(submission)


    def submit(self, submission):
        duplicate = self.dataAccess.find_oldest_submitted_duplicate(submission)
        if duplicate is not None:
            print("duplicate found")
            self.add_comment_to_post(submission, duplicate)
        else:
            print("no duplicate found")
            self.post_submission(submission)


    def post_submission(self, submission):
        title = self.make_submission_title(
            submission.title,
            submission.description,
            config.max_length)
        try:
            print('submitting: ' + title)
            submitted = self.reddit.subreddit(config.subreddit).submit(title, url=submission.url)
            self.dataAccess.submit(submission, submitted)
        except:
            print('error submitting')
            traceback.print_exc()


    def add_comment_to_post(self, submission, duplicate):
        try:
            duplicate_post = self.reddit.submission(id=duplicate.submission_id)
            comment_text = self.make_comment(submission)

            print('commenting: ' + comment_text)
            reply = duplicate_post.reply(comment_text)
            self.dataAccess.submit_duplicate(submission, duplicate, reply)
        except:
            print('error commenting on duplicate post')
            reply = None
            traceback.print_exc()


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

    
    def make_comment(self, submission):
        #markdown for links is [link title](http://link.com)
        comment_text = '[{}{}]({})'.format(
            config.other_source_prefix,
            submission.feed_name,
            submission.url)
        return comment_text


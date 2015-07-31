#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from importer import Importer
from submitter import Submitter
from feeds import feeds

parser = argparse.ArgumentParser(description='Start chreddit tasks')
parser.add_argument('taskname', metavar='task_name', help='The name of the task to run')
args = parser.parse_args()

if (args.taskname) == 'import':
    importer = Importer()
    importer.import_feeds(feeds)

if (args.taskname) == 'submit':
    submitter = Submitter()
    submitter.login()
    submitter.submit_all_unsubmitted()


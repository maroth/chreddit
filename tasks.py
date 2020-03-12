#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from importer import Importer
from submitter import Submitter
import status
from feeds import feeds

from scrapers.watson import WatsonScraper

parser = argparse.ArgumentParser(description='Start chreddit tasks')
parser.add_argument('taskname', metavar='task_name', help='The name of the task to run')
args = parser.parse_args()

if (args.taskname) == 'import':
    importer = Importer()
    importer.import_feeds(feeds)

if (args.taskname) == 'scrape':
    watson = WatsonScraper()
    watson.scrape()

if (args.taskname) == 'submit':
    submitter = Submitter()
    submitter.submit_all_unsubmitted()

if (args.taskname) == 'status':
    print(status.get_status())


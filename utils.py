#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from models import Submission


class Expando(object):
    pass


def create_submission(
        title=u'submission titlé',
        description=u'submission déscription',
        url=u'http://www.url.com/test',
        created=datetime.datetime.now(),
        submitted=datetime.datetime.now(),
        submission_id='3443s',
        duplicate_of=None):

    submission = Submission()
    submission.title = title
    submission.description = description
    submission.url = url
    submission.created = created
    submission.submitted = submitted
    submission.submission_id = submission_id
    submission.duplicate_of = duplicate_of
    return submission

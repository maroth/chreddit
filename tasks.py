import argparse
from importer import Importer
from feeds import feeds

parser = argparse.ArgumentParser(description='Start chreddit tasks')
parser.add_argument('taskname', metavar='task_name', help='The name of the task to run')
args = parser.parse_args()

if (args.taskname) == 'import':
    importer = Importer()
    importer.importFeeds(feeds)


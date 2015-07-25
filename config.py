import os

username = os.environ['REDDIT_USERNAME']
password = os.environ['REDDIT_PASSWORD']
subreddit = os.environ['SUBREDDIT']
database_url = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/chreddit')

#table name for database to store submissions in
tablename = 'submission'

#max rows in database, oldest entries which are more than these are deleted on insert
max_rows = 9500

#reddit constant
max_length = 300

#append when description is too long to fit in max_length
suffix = '...'

#separator between feed title and description in submission title
separator = u'\u2014' 

#number of submissions to post each time the script is run (every ten minutes from heroku)
submissions_per_run = 5

#user agent to send to reddit API when submitting
user_agent = 'submission agent for /r/' + subreddit
